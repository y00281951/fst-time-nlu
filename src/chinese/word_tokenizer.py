# Copyright (c) 2025 Ming Yu (yuming@oppo.com), Liangliang Han (hanliangliang@oppo.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""中文词级分词器。

策略：
- 中文字符维持单字粒度；
- 数字、英文及其它非中文片段复用英文词级逻辑，组成词级 token；
- 长数字使用占位符以避免符号表膨胀。
"""

from __future__ import annotations

import unicodedata
from typing import List, Optional

import pynini

from .global_symbol_table import get_symbol_table


class ChineseWordTokenizer:
    def __init__(self, long_number_threshold: int = 6):
        self.sym = get_symbol_table()
        self.long_number_threshold = long_number_threshold
        self.long_number_token = "__long_number__"
        if self.sym.find(self.long_number_token) == -1:
            self.sym.add_symbol(self.long_number_token)

        self.stats = {
            "total_tokens": 0,
            "unknown_tokens": 0,
            "long_number_tokens": 0,
        }

    # ------------------------------------------------------------------
    # tokenization
    # ------------------------------------------------------------------
    @staticmethod
    def _is_chinese_char(ch: str) -> bool:
        code = ord(ch)
        return 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF or 0x20000 <= code <= 0x2A6DF

    @staticmethod
    def _is_english_letter(ch: str) -> bool:
        return ("A" <= ch <= "Z") or ("a" <= ch <= "z")

    @classmethod
    def simple_tokenize(cls, text: str) -> List[str]:  # noqa: C901
        tokens: List[str] = []
        i = 0
        length = len(text)
        while i < length:
            ch = text[i]
            if ch.isspace():
                tokens.append(" ")
                i += 1
                continue
            if cls._is_chinese_char(ch):
                tokens.append(ch)
                i += 1
                continue
            if ch.isdigit():
                j = i + 1
                while j < length and text[j].isdigit():
                    j += 1
                if j < length and text[j] == "." and (j + 1) < length and text[j + 1].isdigit():
                    k = j + 1
                    while k < length and text[k].isdigit():
                        k += 1
                    tokens.append(text[i:k])
                    i = k
                    continue
                # 非小数：逐位作为独立token，便于与现有数值FST匹配
                while i < j:
                    tokens.append(text[i])
                    i += 1
                continue
            if cls._is_english_letter(ch):
                j = i + 1
                while j < length:
                    cj = text[j]
                    if cls._is_english_letter(cj) or cj.isdigit() or cj in {"'", "-", "_"}:
                        j += 1
                    else:
                        break
                tokens.append(text[i:j].lower())
                i = j
                continue
            # 其它字符（标点、符号等）直接作为独立token
            tokens.append(ch)
            i += 1
        return tokens

    def tokenize(self, text: str) -> List[str]:
        tokens: List[str] = []
        for token in self.simple_tokenize(text.strip()):
            if token == "":
                continue
            if token == " ":
                tokens.append(" ")
                continue

            normalized = token
            if self._looks_like_number(token):
                digits_only = token.replace(".", "")
                if len(digits_only) >= self.long_number_threshold:
                    tokens.append(self.long_number_token)
                    self.stats["long_number_tokens"] += 1
                    self.stats["total_tokens"] += 1
                    continue
            if self.sym.find(normalized) == -1:
                self.stats["unknown_tokens"] += 1
                fallback_tokens = [ch for ch in normalized if self.sym.find(ch) != -1]
                if fallback_tokens:
                    tokens.extend(fallback_tokens)
                    self.stats["total_tokens"] += len(fallback_tokens)
                continue

            tokens.append(normalized)
            self.stats["total_tokens"] += 1
        return tokens

    def _looks_like_number(self, token: str) -> bool:
        if token.isdigit():
            return True
        if token.count(".") == 1:
            left, right = token.split(".", 1)
            return left.isdigit() and right.isdigit()
        return False

    def _ensure_symbol(self, token: str) -> None:
        # 禁用自动扩展全局符号表，仅统计未知token
        return

    # ------------------------------------------------------------------
    def build_input_fst(self, tokens: List[str]) -> pynini.Fst:
        fst = pynini.Fst()
        fst.set_input_symbols(self.sym)
        fst.set_output_symbols(self.sym)
        states = [fst.add_state() for _ in range(len(tokens) + 1)]
        fst.set_start(states[0])
        fst.set_final(states[-1])

        for idx, token in enumerate(tokens):
            token_id = self.sym.find(token)
            if token_id == -1:
                self.stats["unknown_tokens"] += 1
                continue
            arc = pynini.Arc(
                token_id,
                token_id,
                pynini.Weight.one(fst.weight_type()),
                states[idx + 1],
            )
            fst.add_arc(states[idx], arc)
        return fst

    def process_text(self, text: str) -> pynini.Fst:
        tokens = self.tokenize(text)
        return self.build_input_fst(tokens)

    def get_stats(self) -> dict:
        return dict(self.stats)

    def reset_stats(self) -> None:
        for key in self.stats:
            self.stats[key] = 0
