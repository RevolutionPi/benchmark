# piBridge cycle time

This utility is for measuring the cycle time on the piBridge. This is the time
required for a complete update of the IO modules.

Both the module assembly and the MEM configuration of the individual modules
affect the cycle time. This is of great importance for the end user. If a
control program is written with a cycle time of 20 ms, the end user must be able
to rely on the piBridge getting all values synchronized within this time.

## Usage

```
usage: test_cycle_time [-h] [-b] [-d] [-s SECONDS]

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
  -s SECONDS, --seconds SECONDS
                        Measurement time in seconds (1 - 300)
```

## Example

Measure for the period of one second with extended `data_ms` list.

````shell
pibridge_cycle_time.py -d -s1
````

### Shell output (stderr)

````
Hardware configuration (left to right):
	device_RevPiDI_20160818_1_0_002
	device_RevPiDI_20160818_1_0_001
	device_RevPiDO_20160818_1_0_001
	device_RevPiCore_20170404_1_2_001
	device_RevPiAIO_20170301_1_0_001
	device_RevPiAIO_20170301_1_0_002
	device_RevPiMIO_20200901_1_0_001
	device_RevPiDIO_20160818_1_0_001
Cycles:  100 | Min:   20 | Mean:   33.30 | Max:   38 | Remaining:    0 sec.
````

### JSON object (stdout)

```json
{
  "time_local": "2022-11-07T09:42:38.519557",
  "duration_s": 1.0,
  "cycles": 100,
  "min_ms": 20,
  "max_ms": 38,
  "mean_ms": 33.3,
  "module_config": [
    "device_RevPiDI_20160818_1_0_002",
    "device_RevPiDI_20160818_1_0_001",
    "device_RevPiDO_20160818_1_0_001",
    "device_RevPiCore_20170404_1_2_001",
    "device_RevPiAIO_20170301_1_0_001",
    "device_RevPiAIO_20170301_1_0_002",
    "device_RevPiMIO_20200901_1_0_001",
    "device_RevPiDIO_20160818_1_0_001"
  ],
  "data_ms": {
    "1667810557.5276382": 37,
    "1667810557.5376203": 21,
    "1667810557.547624": 21,
    "1667810557.5575373": 21,
    "1667810557.567535": 37,
    "1667810557.5776107": 37,
    "1667810557.5876248": 37,
    "1667810557.597579": 37,
    "1667810557.6086557": 33,
    "1667810557.617543": 33,
    "1667810557.6275227": 33,
    "1667810557.637547": 36,
    "1667810557.6476066": 36,
    "1667810557.6575994": 36,
    "1667810557.6679301": 36,
    "1667810557.678729": 33,
    "1667810557.6875079": 33,
    "1667810557.697812": 33,
    "1667810557.7075205": 36,
    "1667810557.7175438": 36,
    "1667810557.7284818": 36,
    "1667810557.7378602": 36,
    "1667810557.748612": 33,
    "1667810557.757513": 33,
    "1667810557.7678063": 33,
    "1667810557.778259": 36,
    "1667810557.7875838": 36,
    "1667810557.7984617": 36,
    "1667810557.8078141": 36,
    "1667810557.8185725": 33,
    "1667810557.8274908": 33,
    "1667810557.837822": 33,
    "1667810557.8474932": 36,
    "1667810557.8575995": 36,
    "1667810557.8684974": 36,
    "1667810557.8778782": 36,
    "1667810557.8887932": 33,
    "1667810557.8975527": 33,
    "1667810557.907798": 33,
    "1667810557.9185576": 36,
    "1667810557.9284341": 36,
    "1667810557.938757": 36,
    "1667810557.948145": 36,
    "1667810557.9577334": 33,
    "1667810557.9675512": 33,
    "1667810557.9781523": 33,
    "1667810557.9876564": 36,
    "1667810557.9975622": 36,
    "1667810558.0075464": 36,
    "1667810558.0175757": 36,
    "1667810558.0280683": 33,
    "1667810558.0375462": 33,
    "1667810558.0476084": 33,
    "1667810558.059126": 36,
    "1667810558.068189": 36,
    "1667810558.077531": 36,
    "1667810558.0875766": 36,
    "1667810558.099618": 33,
    "1667810558.1076796": 33,
    "1667810558.1175823": 38,
    "1667810558.1276412": 38,
    "1667810558.138288": 38,
    "1667810558.1475635": 38,
    "1667810558.1596482": 21,
    "1667810558.167592": 21,
    "1667810558.177566": 38,
    "1667810558.187595": 38,
    "1667810558.1976585": 20,
    "1667810558.207541": 20,
    "1667810558.2175572": 20,
    "1667810558.2276611": 20,
    "1667810558.2385623": 21,
    "1667810558.2475023": 21,
    "1667810558.257617": 21,
    "1667810558.2675333": 35,
    "1667810558.27755": 35,
    "1667810558.287551": 35,
    "1667810558.297614": 35,
    "1667810558.3075743": 33,
    "1667810558.317549": 33,
    "1667810558.3275304": 33,
    "1667810558.337533": 36,
    "1667810558.3481152": 36,
    "1667810558.357517": 36,
    "1667810558.3675666": 36,
    "1667810558.377597": 33,
    "1667810558.3875473": 33,
    "1667810558.3975425": 33,
    "1667810558.4075174": 36,
    "1667810558.4175713": 36,
    "1667810558.4276812": 36,
    "1667810558.4381473": 36,
    "1667810558.4488904": 33,
    "1667810558.4574978": 33,
    "1667810558.4675725": 33,
    "1667810558.4775057": 36,
    "1667810558.487534": 36,
    "1667810558.4975471": 36,
    "1667810558.5075667": 36,
    "1667810558.518509": 33
  }
}
```