```bash
# Create virtual bridge interfaces for passing traffic
sudo ip link add br0 type bridge
sudo ip link add br1 type bridge

# no shut
sudo ip link set br0 up # kali VM (testing setup)
sudo up link set br1 up # ubuntu VM (testing setup)

# assign some example IPs
sudo ip addr add 192.160.1.1/24 dev br0
sudo ip addr add 192.160.2.1/24 dev br0
```
