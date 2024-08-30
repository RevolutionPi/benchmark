#!/bin/env python3

# SPDX-FileCopyrightText: 2022 KUNBUS GmbH
#
# SPDX-License-Identifier: MIT

import subprocess
import re

exec_match = re.compile(r'(?:total time taken by event execution:\s*)(\d*\.\d*)')
total_match = re.compile(r'(?:total time:\s*)(\d*\.\d*)')

print("{}\t{}\t{}\t{}".format('size', 'threads', 'total_time', 'exec_time'))
for junk in range(64, 1088, 64):
    for threads in range(1, 40):
        result = subprocess.run(['sysbench', '--num-threads='+str(threads), '--test=memory',
                                '--memory-block-size='+str(junk)+'K',
                                '--memory-total-size=1G', 'run'], stdout=subprocess.PIPE)
        output = result.stdout.decode('ascii')
        exec_time = exec_match.search(output).group(1)
        total_time = total_match.search(output).group(1)
        print("{}\t{}\t{}\t{}".format(junk, threads, total_time, exec_time))

# check temperature after stress
# subprocess.run(['vcgencmd', 'measure_temp'])
