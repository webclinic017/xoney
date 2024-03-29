# Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
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
# =============================================================================
from abc import ABC

from xoney.generic.candlestick.candle import Candle
from xoney.generic.trades.levels import Level
from xoney.generic.trades.levels.utils import CheckLevelBreakout


class BaseEntry(Level, ABC):
    def _update_trade_volume(self) -> None:
        if not self.crossed:
            self._trade_volume = self._trade.potential_volume


class SimpleEntry(BaseEntry):
    def check_breaking(self, candle: Candle) -> bool:
        return True


class AveragingEntry(BaseEntry):
    def check_breaking(self, candle: Candle) -> bool:
        return CheckLevelBreakout.against_trade_side(
            level=self,
            candle=candle)
