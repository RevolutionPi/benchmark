# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

from revpi_stress_tester.worker import Worker


class StressWorker(Worker):
    def __init__(self, args: list):
        super(StressWorker, self).__init__(["stress-ng"] + args)


class StressCPUWorker(StressWorker):
    def __init__(self, num_cores: int):
        super().__init__(["-c", str(num_cores)])
        self.name = "stress_cpu"
