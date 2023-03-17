# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

"""Command line interface."""
__author__ = "Nicolai Buchwitz"
__copyright__ = "Copyright (C) 2023 KUNBUS GmbH"
__license__ = "MIT"

import argparse
import getpass
import sys
import threading

from revpi_stress_tester import tools
from revpi_stress_tester.worker import (
    WorkerExecutableNotFound,
    iperf3,
    rt,
    Worker,
    stress,
)


def interval_type(value):
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Interval must be a number")

    if value < 1:
        raise argparse.ArgumentTypeError("Minimum interval is 1 seconds")
    elif value > 60:
        raise argparse.ArgumentTypeError("Maximum interval is 60 seconds")

    return value


def rt_prio_type(value):
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("RT priority must be a number")

    if value < 1:
        raise argparse.ArgumentTypeError("Minimum RT priority is 1")
    elif value > 100:
        raise argparse.ArgumentTypeError("Maximum RT priority is 100")

    return value


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser_stress = parser.add_argument_group("stress-ng specific options")
    parser_stress.add_argument(
        "-c",
        dest="stress_num_cpu_cores",
        metavar="NUMBER_CPU_CORES",
        type=int,
        help="Number of cpu cores used for stress test",
    )

    parser_iperf3 = parser.add_argument_group("iperf3 specific options")
    parser_iperf3.add_argument(
        "-n",
        action="append",
        dest="iperf3_server_interfaces",
        help="Interfaces on which an iperf3 server should listen",
    )
    parser_iperf3.add_argument(
        "-N",
        action="append",
        dest="iperf3_client_ips",
        help="IPs a iperf3 client should connect to",
    )

    parser_rt = parser.add_argument_group("rt-tests specific options")
    parser_rt.add_argument(
        "-p",
        type=rt_prio_type,
        default=90,
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
        type=interval_type,
        default=1,
        help="Interval between each metric measurement",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        dest="log_file",
        help="""A log file where the CSV output ofthe performance
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
        try:
            for worker in self.worker_list:
                worker.start(self.stop_event)

            monitor = tools.PerformanceMonitor()
            print(",".join(monitor.headers()))

            performance_metrics = []
            while not self.stop_event.wait(self.monitor_interval):
                performance_metrics.append(monitor.metrics())

                print(",".join(map(str, performance_metrics[-1])))

        except WorkerExecutableNotFound as we:
            print(
                "Dependency missing: "
                + f"Could not find executable '{we.executable}' in PATH. "
                + "Please refer to setup instructions.",
                file=sys.stderr,
            )

            return 1
        except KeyboardInterrupt:
            self.stop_event.set()

            if self.log_file:
                tools.save_csv_log(
                    self.log_file,
                    performance_metrics,
                    tools.PerformanceMonitor.headers(),
                )

            for worker in self.worker_list:
                worker.join()

            return 0


def main() -> int:
    args = parse_arguments()

    cli = CLI(args.monitor_interval, args.log_file, args.histogram_file)

    if args.stress_num_cpu_cores is not None:
        cli.add_worker(stress.StressCPUWorker(args.stress_num_cpu_cores))

    if args.iperf3_server_interfaces is not None:
        for interface in args.iperf3_server_interfaces:
            cli.add_worker(iperf3.IPerf3ServerWorker(interface))

    if args.iperf3_client_ips is not None:
        for ip in args.iperf3_server_interfaces:
            cli.add_worker(iperf3.IPerf3ClientWorker(ip))

    if args.histogram_file:
        cli.add_worker(rt.CyclicTestWorker(args.rt_prio, args.histogram_file))

    return cli.run()
