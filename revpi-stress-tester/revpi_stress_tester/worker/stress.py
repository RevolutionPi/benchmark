# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

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
