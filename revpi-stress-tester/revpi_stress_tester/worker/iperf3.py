# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

from . import Worker
from .. import tools


class IPerf3Worker(Worker):
    def __init__(self, *args):
        super().__init__("iperf3", *args)


class IPerf3ServerWorker(IPerf3Worker):
    def __init__(self, interface: str, port: int):
        # iperf3 has some issues with link local IPv6, so let's keep it with v4 for the moment
        ip_address = tools.get_ip_addresses(interface, ipv4=True, ipv6=False)[0]
        args = ["-s", "-B", ip_address, "-p", str(port)]

        super().__init__(*args)
        self.name = f"iperf3_server_{interface}_{port}"
