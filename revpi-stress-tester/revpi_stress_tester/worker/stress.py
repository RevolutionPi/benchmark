# SPDX-FileCopyrightText: 2023 KUNBUS GmbH
#
# SPDX-License-Identifier: MIT

from . import Worker


class StressWorker(Worker):
    def __init__(self, *args):
        """
        Stress worker based on stress-ng.

        :param args: pass arguments to stress-ng command
        """
        super().__init__("stress-ng", *args)


class StressCPUWorker(StressWorker):
    def __init__(self, num_cores: int):
        super().__init__("-c", str(num_cores))
        self.name = "stress_cpu"
