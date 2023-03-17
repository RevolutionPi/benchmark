# Hardware Stress Test for Revolution Pi

This tool was developed to analyse the influence of different load scenarios on the temperature development of the RevPi. The CPU cores and network interfaces can be stressed individually or in combination. The tools `stress-ng` (CPU) and `iperf3` (network) are used for this purpose.

During runtime, the CPU temperature, clock speed and the status register, which describes whether the CPU was throttled, are logged together with the time stamp. In addition, the RT cycle time can be logged (using the `cyclictest` program).

## Usage

```
usage: revpi-stress-tester [-h] [-c NUMBER_CPU_CORES]
                           [-n IPERF3_SERVER_INTERFACES]
                           [--iperf3-rx-port IPERF3_RX_PORT]
                           [--iperf3-tx-port IPERF3_TX_PORT] [-p 1-100]
                           [-H HISTOGRAM_FILE] [-i 1-60] [-l LOG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i 1-60               Interval between each metric measurement
  -l LOG_FILE, --log-file LOG_FILE
                        A log file where the CSV output ofthe performance
                        metrics will be written to

stress-ng specific options:
  -c NUMBER_CPU_CORES   Number of cpu cores used for stress test

iperf3 specific options:
  -n IPERF3_SERVER_INTERFACES
                        Interfaces on which an iperf3 server should listen
  --iperf3-rx-port IPERF3_RX_PORT
                        Port on which the iperf3 worker for RX should listen
  --iperf3-tx-port IPERF3_TX_PORT
                        Port on which the iperf3 worker for TX should listen

rt-tests specific options:
  -p 1-100              The RT priority with which cyclictest is run
  -H HISTOGRAM_FILE, --histogram-file HISTOGRAM_FILE
                        A file where the histogram output of the cyclictest
                        will be written to
```

Test options explained:

| Argument           | Description                                                                                                                                         | Example                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `-c NUMBER`        | Spawn `NUMBER` stress-ng workers for generating CPU load                                                                                            | `-c 4`                   |
| `-n INTERFACE`     | Run `iperf3` server instance bound to all IPs (IPv4 and IPv6) of `INTERFACE`. This test will generate load on the RX part of the network interface. | `-n eth0`                |
| `--iperf3-rx-port` | Override the port iperf3 is using for the worker which is ment for RX testing. Defaults to `5201`                                                   | `--iperf3-rx-port 10000` |
| `--iperf3-tx-port` | Override the port iperf3 is using for the worker which is ment for TX testing. Defaults to `5202`                                                   | `--iperf3-tx-port 10001` |

Test monitoring options explain:

| Argument      | Description                                                                                                                                      | Example                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| `-i`          | Interval in seconds, with which the CPU performance and throttling metrics are gathered                                                          | `-i 10`                |
| `-l FILENAME` | A log file where the CSV output of the performance metrics will be written to. This can be used in later reports                                 | `-l my_stresstest.csv` |
| `-H FILENAME` | A file where the histogram output of the cyclictest will be written to. This can be used to compare the rt latencies with different test setups. | `-H my_histogram.csv`  |
| `-p PRIORITY` | The RT priority with which cyclictest is run. Defaults to `90`                                                                                   | `-p 99`                |

## Setup

### DUT

Install dependencies on DUT

```
sudo apt install -y python3-psutil iperf3 stress-ng rt-tests
```

### Workstation (remote for network performance tests)

Install dependencies on your workstation (command can vary on other distributions than Debian):

```
sudo apt install -y iperf3
```

The Iperf3 clients must run in a continuous loop to ensure a continuous utilisation of the server on the RevPi side. This can be archived by wrapping the client command into a while true loop:

Client for RX

```
# change to your setup
DUT_IP=192.168.123.123
while /bin/true; do iperf3 -N -p 5201 -4 -c $DUT_IP; done
```

Client for TX

```
# change to your setup
DUT_IP=192.168.123.123
while /bin/true; do iperf3 -R -N -p 5202 -4 -c $DUT_IP; done
```

## Example: Stress all CPU Cores and network interfaces on a RevPi Connect

> **NOTE: For network performance test an endpoint on the workstation is needed. Please refer to the section Workstation in the setup instructions.**

Start with stress-ng worker on all 4 CPU cores and two iperf3 servers (one for RX one for TX) on each of `eth0` and `eth1`. The cpu performance metrics will be written to `revpi_connect_metrics.csv` and the rt latency histogram to `revpi_connect_rt_histogram.csv`

```
./revpi-stress-tester -c 4 -n eth0 -n eth1 -l revpi_connect_metrics.csv -H revpi_connect_rt_histogram.csv
```

## Data format of CSV Log Files

### CPU Performance Metrics (`--log-file`)

e.g. `./revpi-stress-tester [...] -l my-measurements.csv [...]`


| Column            | Description                                                                                                                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `time`            | Unix timestamp when the measurements where taken                                                                                                                                                         |
| `cpu_temperature` | Core temperature of BCM2XXX SoC (unit `°C`)                                                                                                                                                              |
| `cpu_clock_speed` | Clock frequency of the arm (unit `Hz`)                                                                                                                                                                   |
| `cpu_throttled`   | Staus register which contains information about how and why the CPU was throttled. For more details on the different bits see: https://www.raspberrypi.com/documentation/computers/os.html#get_throttled |

Example:

```
time,cpu_temperature,cpu_clock_speed,cpu_throttled
1679400313,55.5,1500345728,0
1679400314,55.5,1500345728,0
1679400315,55.5,1500398464,0
1679400316,55.5,1500345728,0
[...]
```

### RT Cycle Metrics (`--histogram-file`)

| Column        | Description                                                                                                                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `latency`     | RT latency (unit `μs`)                                                                                                                                                                                                              |
| `count_coreN` | Number of times the latency was measured i.e. iteration count. For each CPU core a separate field is added to the CSV. A machine with 4 CPU cores will therefore list `count_core1`, `count_core2`, `count_core3` and `count_core4` |

Example:

```
latency,core1_count,core2_count,core3_count,core4_count
000000,0,0,0,0
000001,0,0,0,0
000002,0,0,0,0
000003,0,0,0,0
000004,0,0,0,0
000005,0,0,0,0
000006,9,0,0,0
000007,2125,1552,2436,983
000008,1597,2057,1445,1868
000009,564,689,543,926
000010,326,219,182,381
000011,188,154,89,299
000012,69,74,46,145
000013,35,33,23,50
000014,12,34,14,55
000015,18,23,7,24
000016,3,13,3,8
000017,3,10,0,5
[...]
```