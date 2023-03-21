# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

import csv
import socket
import subprocess
import time

import psutil


class PerformanceMonitor:
    def _vcgencmd(self, command: str):
        stdout = subprocess.check_output(["vcgencmd", command])
        return stdout.decode().strip().split("=")[1]

    @property
    def temperature(self):
        # return temperature minus unit
        return float(self._vcgencmd("measure_temp")[:-2])

    @property
    def clock_speed(self):
        return int(self._vcgencmd("measure_clock arm"))

    @property
    def throttled(self):
        return int(self._vcgencmd("get_throttled"), base=16)

    @staticmethod
    def headers():
        return "time", "cpu_temperature", "cpu_clock_speed", "cpu_throttled"

    def metrics(self):
        return [int(time.time()), self.temperature, self.clock_speed, self.throttled]


def get_network_interfaces() -> list:
    return list(psutil.net_if_addrs().keys())


def get_ipv6_addresses(interface: str):
    return get_ip_addresses(interface, ipv4=False)


def get_ipv4_addresses(interface: str):
    return get_ip_addresses(interface, ipv6=False)


def get_ip_addresses(interface: str, ipv4: bool = True, ipv6: bool = True):
    ip_types = []

    if ipv6:
        ip_types.append(socket.AF_INET6)
    if ipv4:
        ip_types.append(socket.AF_INET)

    addresses = []
    for interface_address in psutil.net_if_addrs().get(interface, []):
        if interface_address.family in ip_types:
            addresses.append(interface_address.address)

    if not addresses:
        raise Exception(f"Could not determine ip address for interface: {interface}")

    return addresses


def bucket(line):
    line = line.strip()

    # skip empty lines or ones starting with a comment
    if line.startswith("#") or not line:
        return

    try:
        latency, numbers_per_core = line.split(" ")

        return [latency] + list(map(int, numbers_per_core.split("\t")))
    except ValueError:
        return


def save_csv_log(filename: str, data: list, headers: list = None):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)

        if headers is not None:
            writer.writerow(headers)

        writer.writerows(data)
