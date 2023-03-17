# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

"""Command line interface."""
__author__ = "Nicolai Buchwitz"
__copyright__ = "Copyright (C) 2023 KUNBUS GmbH"
__license__ = "MIT"

import argparse
import getpass
import signal
import sys
import threading

from . import tools
from .worker import Worker, WorkerExecutableNotFound, iperf3, rt, stress


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser_stress = parser.add_argument_group("stress-ng specific options")
    parser_stress.add_argument(
        "-c",
        default=0,
        dest="stress_num_cpu_cores",
        metavar="NUMBER_CPU_CORES",
        type=int,
        help="Number of cpu cores used for stress test",
    )

    parser_iperf3 = parser.add_argument_group("iperf3 specific options")
    parser_iperf3.add_argument(
        "-n",
        action="append",
        default=[],
        type=str,
        dest="iperf3_server_interfaces",
        help="Interfaces on which an iperf3 server should listen",
    )
    parser_iperf3.add_argument(
        "--iperf3-rx-port",
        default=5201,
        type=int,
        dest="iperf3_rx_port",
        help="Port on which the iperf3 worker for RX should listen",
    )
    parser_iperf3.add_argument(
        "--iperf3-tx-port",
        default=5202,
        type=int,
        dest="iperf3_tx_port",
        help="Port on which the iperf3 worker for TX should listen",
    )

    parser_rt = parser.add_argument_group("rt-tests specific options")
    parser_rt.add_argument(
        "-p",
        type=int,
        default=90,
        choices=range(1, 101),
        metavar="1-100",
        dest="rt_prio",
        help="The RT priority with which cyclictest is run",
    )
    parser_rt.add_argument(
        "-H",
        "--histogram-file",
        dest="histogram_file",
        help="""A file where the histogram output of the cyclyctest
        will be written to""",
    )

    parser.add_argument(
        "-i",
        dest="monitor_interval",
        type=int,
        default=1,
        choices=range(1, 61),
        metavar="1-60",
        help="Interval between each metric measurement",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        dest="log_file",
        help="""A log file where the CSV output of the performance
        metrics will be written to""",
    )

    args = parser.parse_args()

    if getpass.getuser() != "root":
        parser.error("Program needs to be run as superuser root")

    return args


class CLI:
    def __init__(
        self,
        monitor_interval: int = 1,
        log_file: str = None,
        histogram_file: str = None,
    ) -> None:
        self.worker_list = []
        self.stop_event = threading.Event()

        self.monitor_interval = monitor_interval
        self.log_file = log_file
        self.histogram_file = histogram_file

    def add_worker(self, worker: Worker) -> None:
        self.worker_list.append(worker)

    def run(self) -> int:
        for worker in self.worker_list:
            worker.start()

        monitor = tools.PerformanceMonitor()
        print(",".join(monitor.headers()))

        performance_metrics = []
        while not self.stop_event.wait(self.monitor_interval):
            performance_metrics.append(monitor.metrics())
            print(",".join(map(str, performance_metrics[-1])))

        if self.log_file:
            tools.save_csv_log(
                self.log_file,
                performance_metrics,
                tools.PerformanceMonitor.headers(),
            )

        for worker in self.worker_list:
            worker.stop()

        for worker in self.worker_list:
            worker.join()

        return 0


def main() -> int:
    args = parse_arguments()

    cli = CLI(args.monitor_interval, args.log_file, args.histogram_file)

    # Catch events to set the stop signal from control+c or SIGINT from OS
    signal.signal(signal.SIGINT, lambda n, f: cli.stop_event.set())
    signal.signal(signal.SIGTERM, lambda n, f: cli.stop_event.set())

    try:
        if args.stress_num_cpu_cores > 0:
            cli.add_worker(stress.StressCPUWorker(args.stress_num_cpu_cores))

        for interface in args.iperf3_server_interfaces:
            cli.add_worker(iperf3.IPerf3ServerWorker(interface, args.iperf3_rx_port))
            cli.add_worker(iperf3.IPerf3ServerWorker(interface, args.iperf3_tx_port))

        if args.histogram_file:
            cli.add_worker(rt.CyclicTestWorker(args.rt_prio, args.histogram_file))

    except WorkerExecutableNotFound as we:
        # This will happen, if the worker can not find the test command on the system
        print(
            "Dependency missing: "
            + f"Could not find executable '{we.executable}' in PATH. "
            + "Please refer to setup instructions.",
            file=sys.stderr,
        )

        return 1

    return cli.run()
