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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from __future__ import annotations

from xoney.generic.candlestick import Chart, Candle
from xoney.generic.workers import Worker
from xoney.generic.trades import TradeHeap
from xoney.generic.events import Event
from xoney.strategy import Strategy
from xoney.generic.equity import Equity
from xoney.generic.timeframes import TimeFrame, DAY_1

from typing import Iterable


class Backtester(Worker):  # TODO
    _equity: Equity

    @property
    def equity(self) -> Equity:
        return self._equity

    @property
    def free_balance(self) -> float:
        return self._free_balance

    def __init__(self,
                 strategies: Iterable[Strategy]):
        self._strategies = list(strategies)

    def __handle_closed_trades(self) -> None:
        self._free_balance += self._trades.closed.profit
        self._trades.cleanup_closed()

    def run(self,
            chart: Chart,
            initial_depo: float | int,
            commission: float,
            timeframe: TimeFrame = DAY_1) -> None:
        self._free_balance = initial_depo
        self._trades = TradeHeap()
        self.commission = commission

        self._equity = Equity([], timeframe=timeframe)
        self._equity._set_timestamp(chart.timestamp)

        event: Event
        candle: Candle
        events: Iterable[Event] = []
        for e, candle in enumerate(chart, start=1):
            for strategy in self._strategies:
                strategy.run(chart[:e])

                for event in events:
                    event.set_worker(self)
                    event.handle_trades(self._trades)

                self._trades.update_trades(candle=candle)
                self.__handle_closed_trades()

                events = strategy.fetch_events()

            self._equity.append(self.total_balance)
