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
from __future__ import annotations

from abc import abstractproperty, abstractmethod, ABC

class Worker(ABC):
    @abstractmethod
    def run(self,
            *args,
            **kwargs) -> None:  # pragma: no cover
        ...

    @abstractproperty
    def equity(self):  # pragma: no cover
        ...

    @property
    def opened_trades(self):
        return len(self._trades.active)

    @property
    def total_balance(self):
        PnL: float = self._trades.profit

        return self.free_balance + self.used_balance + PnL

    @property
    def used_balance(self):
        return self._trades.potential_volume

    @abstractproperty
    def free_balance(self):  # pragma: no cover
        ...

    @property
    def filled_balance(self):
        return self._trades.filled_volume
