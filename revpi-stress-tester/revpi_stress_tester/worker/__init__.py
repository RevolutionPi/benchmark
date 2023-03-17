# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

import distutils.spawn
import signal
import subprocess
import sys
import threading


class WorkerExecutableNotFound(Exception):
    def __init__(self, command: str) -> None:
        super().__init__(f"Could not find executable: {command[0]}")
        self.command = command
        self.executable = command[0]


class Worker(threading.Thread):
    def __init__(self, cmd: list):
        super(Worker, self).__init__(daemon=True)
        self.cmd = cmd
        self.name = "worker"
        self.stdout = None
        self.stderr = None
        self.stop_event = None

        # check if executable can be found in PATH
        if not distutils.spawn.find_executable(self.cmd[0]):
            raise WorkerExecutableNotFound(self.cmd)

    def start(self, stop_event: threading.Event) -> None:
        self.stop_event = stop_event

        return super().start()

    def run(self):
        proc = None

        while not self.stop_event.wait(timeout=0.5):
            if proc is None or proc.poll() is not None:
                # check if proc was already started, but exited somehow
                if proc is not None:
                    rc = proc.poll()
                    print(
                        f"{self.name} workers child process exited with rc={rc}",
                        file=sys.stderr,
                    )

                # (re)start workers child process (if it has died)
                proc = subprocess.Popen(
                    self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

        # gracefully stop program
        proc.send_signal(signal.SIGTERM)

        # save stdout and stderr output for later usage
        self.stdout = proc.stdout.readlines()
        self.stderr = proc.stderr.readlines()
