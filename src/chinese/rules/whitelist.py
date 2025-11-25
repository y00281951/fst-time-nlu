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

from ...core.processor import Processor
from ...core.utils import get_abs_path
from ..word_level_pynini import string_file, accep, pynutil
from .base.date_base import DateBaseRule

delete = pynutil.delete
insert = pynutil.insert


class WhitelistRule(Processor):
    """白名单规则处理器，处理预定义的时间表达式"""

    def __init__(self):
        super().__init__(name="whitelist")
        self.build_tagger()

    def build_tagger(self):
        whitelist = string_file(get_abs_path("../data/default/whitelist.tsv"))

        shiyi_num = self._build_shiyi_num()
        anti_noon = DateBaseRule().build_anti_noon_rule()

        # 对于whitelist，如果第二列是token类型，则使用该类型；否则使用默认的whitelist类型
        # 使用add_tokens来自动处理类型映射
        tagger = (insert('value: "') + (whitelist | shiyi_num | anti_noon)) + insert('"')
        self.tagger = self.add_tokens(tagger)

    def _build_shiyi_num(self):
        postfix = accep("十") + accep("一")
        prefix = (
            accep("一")
            | accep("二")
            | accep("三")
            | accep("四")
            | accep("五")
            | accep("六")
            | accep("七")
            | accep("八")
            | accep("九")
            | accep("十")
        )
        shiyi_num = prefix + postfix

        return shiyi_num
