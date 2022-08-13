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

from xoney.generic.candlestick import utils

import numpy as np


class Equity:
    def as_array(self):
        return np.array(self._list)

    def __init__(self, iterable):
        self._list = list(iterable)

    def append(self, balance):
        self._list.append(balance)

    def update(self, balance):
        """

        Replaces the last value of the deposit in equity
        """
        self._list[-1] = balance

    def _set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def __getitem__(self, item):
        item = utils.to_int_index(item=item, timestamp=self._timestamp)
        return self._list[item]

    def __op(self, fn, other):
        if isinstance(other, Equity):
            other = other.as_array()
        return Equity(fn(self.as_array(), other))

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
