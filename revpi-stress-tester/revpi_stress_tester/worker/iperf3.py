# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

import ipaddress

from . import Worker
from .. import tools


class IPerf3Worker(Worker):
    def __init__(self, *args):
        super().__init__("iperf3", *args)


class IPerf3ServerWorker(IPerf3Worker):
    def __init__(self, interface: str):
        args = ["-s"]
        for ip in tools.get_ip_addresses(interface):
            args += ["-B", ip]
        super().__init__(*args)
        self.name = f"iperf3_server_{interface}"


class IPerf3ClientWorker(IPerf3Worker):
    def __init__(self, server_ip: str):
        try:
            ip = ipaddress.IPv4Address(server_ip)
        except ipaddress.AddressValueError:
            raise Exception(f"Invalid IP address format for iperf3 server: {server_ip}")

        super().__init__("-c", str(ip))
        self.name = f"iperf3_client_{ip}"

    def run(self):
        # repeat until killed
        while self.stop_event.is_set():
            super().run()
