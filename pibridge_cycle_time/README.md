# piBridge cycle time

This utility is for measuring the cycle time on the piBridge. This is the time
required for a complete update of the IO modules.

Both the module assembly and the MEM configuration of the individual modules
affect the cycle time. This is of great importance for the end user. If a
control program is written with a cycle time of 20 ms, the end user must be able
to rely on the piBridge getting all values synchronized within this time.

## Usage

```
usage: test_cycle_time [-h] [-b] [-d] [-s 1-300]

Measure the cycle time of piControl to update all IO modules.

The value of the variable `RevPiIOCycle` is read from the process
image every 10 milliseconds over the duration of the test. At the end,
a JSON object is output, which contains statistical data and
optionally all measurements with a time stamp.

The runtime status of this program goes to stderr. You will get the JSON
string in the end of measurement on stdout.

optional arguments:
  -h, --help            show this help message and exit
  -b, --batch           Print JSON string only (errors still written to
                        stderr)
  -d, --data            Add measured values with timestamps to JSON output
  -s 1-300, --seconds 1-300
                        Measurement time in seconds
```

## Example

Measure for the period of one second with extended `data_ms` list.

````shell
pibridge_cycle_time.py -d -s1
````

### Shell output (stderr)

````
Hardware configuration (left to right):
	device_RevPiAIO_20170301_1_0_001
	device_RevPiDIO_20160818_1_0_001
	device_RevPiConnect_20171023_1_0_001
Cycles:  100 | Min:    5 | Mean:    5.01 | Max:    6 | Remaining:    0 sec.
````

### JSON object (stdout)

```json
{
  "time_local": "2022-11-09T07:20:08.035959",
  "duration_s": 1.0,
  "cycles": 100,
  "min_ms": 5,
  "max_ms": 6,
  "mean_ms": 5.01,
  "module_config": [
    "device_RevPiAIO_20170301_1_0_001",
    "device_RevPiDIO_20160818_1_0_001",
    "device_RevPiConnect_20171023_1_0_001"
  ],
  "system": {
    "kernel_version": "#1 SMP PREEMPT_RT Thu, 28 Jul 2022 10:36:48 +0200",
    "kernel_release": "5.10.120-rt70-v7",
    "machine": "armv7l"
  },
  "data_ms": {
    "1667974807.045": 5,
    "1667974807.056": 5,
    "1667974807.065": 5,
    "1667974807.076": 5,
    "1667974807.086": 5,
    "1667974807.095": 5,
    "1667974807.105": 5,
    "1667974807.115": 5,
    "1667974807.125": 5,
    "1667974807.135": 5,
    "1667974807.145": 5,
    "1667974807.155": 5,
    "1667974807.165": 5,
    "1667974807.175": 5,
    "1667974807.185": 5,
    "1667974807.195": 5,
    "1667974807.206": 5,
    "1667974807.216": 5,
    "1667974807.225": 5,
    "1667974807.236": 5,
    "1667974807.245": 5,
    "1667974807.255": 5,
    "1667974807.265": 5,
    "1667974807.275": 5,
    "1667974807.285": 5,
    "1667974807.295": 5,
    "1667974807.305": 5,
    "1667974807.315": 5,
    "1667974807.325": 5,
    "1667974807.336": 5,
    "1667974807.346": 5,
    "1667974807.355": 5,
    "1667974807.366": 5,
    "1667974807.376": 5,
    "1667974807.385": 5,
    "1667974807.395": 5,
    "1667974807.405": 5,
    "1667974807.415": 5,
    "1667974807.425": 5,
    "1667974807.435": 5,
    "1667974807.445": 5,
    "1667974807.455": 5,
    "1667974807.465": 5,
    "1667974807.475": 5,
    "1667974807.485": 5,
    "1667974807.495": 5,
    "1667974807.505": 5,
    "1667974807.515": 5,
    "1667974807.526": 5,
    "1667974807.535": 5,
    "1667974807.545": 5,
    "1667974807.555": 5,
    "1667974807.565": 5,
    "1667974807.575": 5,
    "1667974807.585": 5,
    "1667974807.595": 5,
    "1667974807.605": 5,
    "1667974807.615": 5,
    "1667974807.625": 5,
    "1667974807.635": 5,
    "1667974807.645": 5,
    "1667974807.655": 5,
    "1667974807.665": 5,
    "1667974807.675": 5,
    "1667974807.685": 5,
    "1667974807.695": 5,
    "1667974807.705": 5,
    "1667974807.715": 5,
    "1667974807.725": 5,
    "1667974807.735": 5,
    "1667974807.745": 6,
    "1667974807.755": 5,
    "1667974807.765": 5,
    "1667974807.775": 5,
    "1667974807.785": 5,
    "1667974807.795": 5,
    "1667974807.805": 5,
    "1667974807.815": 5,
    "1667974807.826": 5,
    "1667974807.835": 5,
    "1667974807.846": 5,
    "1667974807.856": 5,
    "1667974807.865": 5,
    "1667974807.875": 5,
    "1667974807.885": 5,
    "1667974807.895": 5,
    "1667974807.905": 5,
    "1667974807.915": 5,
    "1667974807.925": 5,
    "1667974807.935": 5,
    "1667974807.945": 5,
    "1667974807.955": 5,
    "1667974807.965": 5,
    "1667974807.976": 5,
    "1667974807.986": 5,
    "1667974807.995": 5,
    "1667974808.006": 5,
    "1667974808.015": 5,
    "1667974808.025": 5,
    "1667974808.035": 5
  }
}
```