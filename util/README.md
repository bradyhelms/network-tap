
<h1 align="center">
  <br>
    Group 15 Senior Project Software Example 
  <br>
</h1>

<h4 align="center">Software testing for our FPGA-based inline network tap.</h4>

<p align="center">
  <a href="#currentabilities">Current Abilities</a>
  <a href="#buildinstructions">Build Instructions</a>
</p>

## Current Abilities 
* Intercept traffic from your computer's onboard NIC
* Adjust the destination MAC address of a real packet


## Build Instructions

```bash
# Clone this repository
$ gh repo clone bradyhelms/Packet-Analyzer-Senior-Project

# cd into the repository
$ cd Packet-Analyzer-Senior-Project

# Run CMake
$ cmake -S . -B build

# Build
$ cmake --build build

# If everything builds successfully, run using:
$ sudo ./PacketAnalyzer [OPTIONS]

# If you need help, run the executable without args to print usage.
$ sudo ./PacketAnalyzer
```
