# Copyright (c) 2025 Ming Yu (yuming@oppo.com)
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

from __future__ import annotations

import logging
from typing import List, Dict, Any

import pynini
from pynini.lib.pynutil import add_weight
from importlib_resources import files

from ..core.processor import Processor
from ..core.logger import get_logger
from .global_symbol_table import get_symbol_table, get_input_tokens
from .word_tokenizer import ChineseWordTokenizer
from .rules import PreProcessor
from .rules.and_rule import AndRule
from .rules import (
    BetweenRule,
    DeltaRule,
    HolidayRule,
    LunarRule,
    PeriodRule,
    RelativeRule,
    UTCTimeRule,
    WeekRule,
    WhitelistRule,
    DecimalRule,
    UnitRule,
    VerbDurationRule,
    RangeRule,
    DeltaTimeAttachRule,
    RecurringRule,
)


class Normalizer(Processor):
    def __init__(
        self,
        cache_dir=None,
        overwrite_cache=False,
        remove_interjections=True,
        traditional_to_simple=True,
        remove_puncts=False,
        full_to_half=True,
        tag_oov=False,
        use_word_level: bool = True,
    ):
        super().__init__(name="zh_normalizer")
        self.logger = get_logger(__name__)
        self.remove_interjections = remove_interjections
        self.traditional_to_simple = traditional_to_simple
        self.remove_puncts = remove_puncts
        self.full_to_half = full_to_half
        self.tag_oov = tag_oov
        self.use_word_level = use_word_level
        self.word_tokenizer = None  # 先设为None，在build_fst后再初始化

        if cache_dir is None:
            cache_dir = str(files("src.chinese.test").joinpath("fst"))
        self.build_fst("zh_tn", cache_dir, overwrite_cache)

        # 在build_fst之后初始化word_tokenizer，确保使用扩展后的符号表
        if use_word_level:
            try:
                self.word_tokenizer = ChineseWordTokenizer()
                self.logger.info(
                    f"中文词级FST已启用，SymbolTable大小: {self.word_tokenizer.sym.num_symbols()}"
                )
            except Exception as e:
                self.logger.warning(f"中文词级FST初始化失败，回退到字符级: {e}")
                self.word_tokenizer = None

    def tag(self, text: str) -> List[Dict[str, Any]]:
        if not text:
            return []
        result = super().tag(text)
        if result:
            return result
        # 词级规则未匹配，回退为逐字符输出
        fallback = []
        for ch in text:
            if ch.isspace():
                continue
            fallback.append({"type": "char", "value": ch})
        return fallback

    def _tag_single(self, text: str) -> List[Dict[str, Any]]:  # noqa: C901
        if self.word_tokenizer:
            try:
                escaped_text = self.word_tokenizer.process_text(text)

                input_sym = escaped_text.input_symbols()
                tagger_input_sym = self.tagger.input_symbols()

                if input_sym and not tagger_input_sym:
                    escaped_text = pynini.accep(text)
                elif (
                    input_sym
                    and tagger_input_sym
                    and input_sym.num_symbols() != tagger_input_sym.num_symbols()
                ):
                    escaped_text = pynini.accep(text)
            except Exception as e:
                logger = logging.getLogger(f"fst_time-{self.name}")
                logger.debug(f"词级处理失败，回退到字符级: {e}")
                escaped_text = pynini.accep(text)
        else:
            escaped_text = pynini.accep(text)

        try:
            lattice = escaped_text @ self.tagger
            if lattice.num_states() == 0:
                return []

            from pynini import shortestpath

            shortest = shortestpath(lattice, nshortest=1)
            if shortest.num_states() == 0:
                return []

            if self.word_tokenizer and shortest.output_symbols():
                try:
                    sym = shortest.output_symbols()
                    tagged_text = shortest.string(token_type=sym)
                except Exception as e:
                    logger = logging.getLogger(f"fst_time-{self.name}")
                    logger.warning(f"词级FST string(token_type=sym)失败: {e}, 文本: {text[:50]}")
                    return []
            else:
                try:
                    tagged_text = shortest.string()
                except Exception as e:
                    logger = logging.getLogger(f"fst_time-{self.name}")
                    logger.warning(f"FST string()失败: {e}, 文本: {text[:50]}")
                    return []

            if not tagged_text:
                return []

            return self.parse_tags(tagged_text)
        except Exception as e:
            logger = logging.getLogger(f"fst_time-{self.name}")
            logger.warning(f"FST匹配失败: {e}, 文本: {text[:50]}")
            return []

    def build_tagger(self):
        # 临时禁用预处理（繁体转简、标点等），直接使用规则组合
        # processor = PreProcessor(
        #     traditional_to_simple=self.traditional_to_simple).processor

        # 阶段1优化：调整权重和顺序，按匹配频率排序
        # 权重越小优先级越高（pynini的shortestpath选择权重最小的路径）
        utctime = add_weight(
            UTCTimeRule().tagger, 0.90
        )  # 最高优先级：年月日时分秒（31.8%+30.7%+15.5%）
        relative_day = add_weight(RelativeRule().tagger, 0.91)  # 高优先级：明天、昨天等
        period = add_weight(PeriodRule().tagger, 0.92)  # 高优先级：上午、下午、晚上（12.1%）
        delta = add_weight(DeltaRule().tagger, 0.93)  # 高优先级：X天前、X小时后（11.0%+8.5%）
        weekday = add_weight(WeekRule().tagger, 0.94)  # 常见：周一、星期二
        between = add_weight(BetweenRule().tagger, 0.95)  # 时间区间
        holiday = add_weight(
            HolidayRule().tagger, 0.96
        )  # 节假日（提高优先级，确保"大年三十"优先匹配为节假日）
        lunar = add_weight(LunarRule().tagger, 0.97)  # 农历
        recurring = add_weight(RecurringRule().tagger, 0.98)  # 周期规则
        range_rule = add_weight(
            RangeRule().tagger, 0.915
        )  # 提高优先级，确保"最近的+X+单位"优先匹配为time_range（高于period的0.92）  # 范围规则
        unit = add_weight(UnitRule().tagger, 1.00)  # 单位（确保"数字-数字+单位"优先匹配）
        delta_time_attach = add_weight(DeltaTimeAttachRule().tagger, 1.01)  # 附加时间
        verb_duration = add_weight(VerbDurationRule().tagger, 1.02)  # 动词持续时间
        whitelist = add_weight(WhitelistRule().tagger, 1.03)  # 白名单
        and_rule = add_weight(AndRule().tagger, 1.04)  # and连接
        decimal = add_weight(DecimalRule().tagger, 1.3)  # 小数

        # 🔧 关键修复：构建skip_rule使用固定的"none"输出，避免动态添加符号
        sym = get_symbol_table()
        # 构建skip_rule：使用词级token拼接（简单版本）
        from .word_level_pynini import pynutil as word_pynutil, accep

        # 收集符号表中的所有token（移除长度限制，支持多字符token）
        skip_arcs = []
        for idx in range(1, sym.num_symbols()):
            token = sym.find(idx)
            if (
                not token
                or token == "<eps>"
                or token.startswith("char { value:")
                # 移除 len(token) > 1 限制，支持所有长度的token
                # 这样可以兜底符号表中的多字符token（如"to"、"tag"等），避免FST失败
            ):
                continue

            # 使用词级insert拼接3个token：
            # 'char{value:"' + token + '"}'
            arc = word_pynutil.insert('char{value:"') + accep(token) + word_pynutil.insert('"}')
            skip_arcs.append(arc)

        # Union所有token的规则（一次性union，避免O(n²)复杂度）
        if skip_arcs:
            skip_rule = pynini.union(*skip_arcs).optimize()
        else:
            skip_rule = pynini.Fst()

        skip_rule = add_weight(skip_rule, 50)  # 与旧版本CharRule对齐

        combined = (
            utctime
            | relative_day
            | period
            | delta
            | weekday
            | between
            | holiday
            | lunar
            | recurring
            | range_rule
            | unit
            | delta_time_attach
            | verb_duration
            | whitelist
            | and_rule
            | decimal
            | skip_rule
        ).optimize()

        # 仍以utc规则为主进行验证，只对该组合取闭包
        tagger = combined.star

        # 简化ε并保持FST优化
        tagger = tagger.rmepsilon().optimize()

        # 词级FST：闭包后手动恢复符号表，保持与英文实现一致
        if self.use_word_level:
            sym = get_symbol_table()
            tagger.set_input_symbols(sym)
            tagger.set_output_symbols(sym)

        self.tagger = tagger
