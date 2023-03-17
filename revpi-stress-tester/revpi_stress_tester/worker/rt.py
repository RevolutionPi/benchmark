# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

import os

from revpi_stress_tester import tools
from revpi_stress_tester.worker import Worker


class CyclicTestWorker(Worker):
    def __init__(self, prio: int, log: str = None):
        histogram_size = 100
        interval = 200

        args = [
            "-q",
            "-m",
            "-S",
            "-p",
            str(prio),
            "-h",
            str(histogram_size),
            "-i",
            str(interval),
        ]

        super(CyclicTestWorker, self).__init__(["cyclictest"] + args)

        self.log = log

    def run(self):
        super().run()

        if self.log is not None:
            self.save_log()

    def save_log(self):
        cpu_cores = os.cpu_count()

        csv_headers = ["latency"]
        csv_headers += [f"count_core{number+1}" for number in range(cpu_cores)]

        tools.save_csv_log(
            self.log,
            self.histogram(),
            csv_headers,
        )

    def histogram(self):
        buckets = []
        for line in self.stdout:
            if line is None:
                continue

            bucket = tools.bucket(line.decode())

            if bucket is not None:
                buckets.append(bucket)

        return buckets
