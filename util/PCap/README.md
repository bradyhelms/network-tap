
<h1 align="center">
  <br>
    Group 15 Senior Project Software Example 
  <br>
</h1>

<h4 align="center">Software testing for our FPGA-based inline network tap.</h4>

## Current Abilities 
* Intercept traffic from your computer's onboard NIC
* Adjust the destination MAC address of a real packet


## Build Instructions

```bash
# cd into the repository
$ cd util/PCap 

# Run CMake
$ cmake -S . -B build

# Build
$ cmake --build build

# If everything builds successfully, run using:
$ sudo ./PacketAnalyzer [OPTIONS]

# If you need help, run the executable without args to print usage.
$ sudo ./PacketAnalyzer
```
