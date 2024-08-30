#!/bin/env python3

# SPDX-FileCopyrightText: 2022 KUNBUS GmbH
#
# SPDX-License-Identifier: MIT

import subprocess
import re

exec_match = re.compile(r'(?:total time taken by event execution:\s*)(\d*\.\d*)')
total_match = re.compile(r'(?:total time:\s*)(\d*\.\d*)')

for x in range(1, 40):
    result = subprocess.run(['sysbench', '--num-threads='+str(x), '--test=cpu',
                             '--cpu-max-prime=5000', 'run'],
                             stdout=subprocess.PIPE)
    output = result.stdout.decode('ascii')
    exec_time = exec_match.search(output).group(1)
    total_time = total_match.search(output).group(1)
    print("{}\t{}\t{}".format(x, total_time, exec_time))

# check temperature after stress
# subprocess.run(['vcgencmd', 'measure_temp'])
