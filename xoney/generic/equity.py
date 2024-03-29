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
import operator

from xoney.analysis.metrics import evaluate_metric
from xoney.generic._series import TimeSeries
from xoney.generic.candlestick import _utils
from xoney.generic.timeframes import DAY_1

import numpy as np


class Equity(TimeSeries):
    def as_array(self):
        return np.array(self._list)

    def __init__(self,
                 iterable,
                 timestamp=None,
                 timeframe=DAY_1):
        if timestamp is None:
            timestamp = []
        self.timeframe = timeframe
        self._timestamp = timestamp
        self._list = list(iterable)

    def __eq__(self, other):
        if not isinstance(other, Equity):
            raise TypeError(f"Object is not Equity: {other}")
        if any(other.as_array() != self.as_array()):
            return False
        if self.timeframe != other.timeframe:
            return False
        return True

    def append(self, balance):
        self._list.append(balance)

    def update(self, balance):
        """

        Replaces the last value of the deposit in equity
        """
        self._list[-1] = balance

    def change(self):
        array = self.as_array()
        diff = np.diff(array, prepend=0.0)
        change = diff / array
        return self.__class__(iterable=change,
                              timeframe=self.timeframe,
                              timestamp=self._timestamp)

    def log(self):
        return self.__class__(iterable=np.log(self._list),
                              timeframe=self.timeframe,
                              timestamp=self._timestamp)

    def mean(self):
        return self.as_array().mean()

    def std(self):
        return self.as_array().std()

    def __getitem__(self, item):
        item = _utils.to_int_index(item=item,
                                   timestamp=self._timestamp)
        if isinstance(item, slice):
            return self.__class__(iterable=self._list[item],
                                  timestamp=self._timestamp[item],
                                  timeframe=self.timeframe)
        return self._list[item]

    def __op(self, fn, other):
        if isinstance(other, Equity):
            other = other.as_array()
        return self.__class__(
            iterable=fn(self.as_array(), other),
            timestamp=self._timestamp,
            timeframe=self.timeframe
        )

    def __add__(self, other):
        return self.__op(operator.add, other)

    def __sub__(self, other):
        return self.__op(operator.sub, other)

    def __mul__(self, other):
        return self.__op(operator.mul, other)

    def __truediv__(self, other):
        return self.__op(operator.truediv, other)

    def __iter__(self):
        for deposit in self._list:
            yield deposit

    def __len__(self):
        return len(self._list)

    def evaluate(self, metric):
        return evaluate_metric(metric=metric,
                               equity=self)
