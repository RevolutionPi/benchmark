# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright 2023 KUNBUS GmbH

import shutil
import signal
import subprocess
import sys
import threading
from subprocess import TimeoutExpired


class WorkerExecutableNotFound(Exception):
    def __init__(self, command: list) -> None:
        super().__init__(f"Could not find executable: {command[0]}")
        self.command = command
        self.executable = command[0]


class Worker(threading.Thread):
    def __init__(self, cmd: str, *cmd_args):
        """
        Base worker class, which all worker must inherit from.

        :param cmd: Command to execute for this worker
        :param cmd_args: Arguments to pass to command
        """
        super().__init__(daemon=True)
        self.cmd = [cmd] + list(cmd_args)
        self.name = "worker"
        self.stdout = None
        self.stderr = None
        self.stop_event = threading.Event()

        # Check if executable can be found in PATH
        if not shutil.which(self.cmd[0]):
            raise WorkerExecutableNotFound(self.cmd)

    def stop(self) -> None:
        """Stop this worker."""
        self.stop_event.set()

    def run(self):
        proc = None

        while not self.stop_event.wait(timeout=0.5):
            if proc is None or proc.poll() is not None:
                # Check if proc was already started, but exited somehow
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

        # Gracefully stop program
        proc.send_signal(signal.SIGTERM)

        try:
            proc.wait(5.0)
        except TimeoutExpired:
            # Program has not terminated within 5 seconds, so we need to kill it
            proc.kill()

        # Save stdout and stderr output for later usage
        self.stdout = proc.stdout.readlines()
        self.stderr = proc.stderr.readlines()
