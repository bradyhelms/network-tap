import getopt
import sys
import pyshark
import json
from collections import Counter

def print_usage():
    print(
        """Usage: python3 summary.py [OPTIONS] [INPUT_FILE]
            -h, --help      Print this help dialog
            -j, --json      Output summary as JSON
            -s, --summary   Output summary in human readable format""")
    exit(0)

class PacketSummary:
    def __init__(self, frame_number, timestamp, protocol, src_ip, dst_ip, length):
        self.frame_number = frame_number
        self.timestamp = timestamp
        self.protocol = protocol
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.length = length

    def __str__(self):
        return f"Frame {self.frame_number}: {self.protocol} {self.src_ip} -> {self.dst_ip}, Length: {self.length}"

## CLAs
json_flag = False
full_flag = False
argument_list = sys.argv[1:]
options = "jsh"
long_options = ["json", "summary", "help"]

if len(argument_list) == 0:
    print_usage()

try:
    arguments, values = getopt.getopt(argument_list, options, long_options)
    for current_arg, current_val in arguments:
        if current_arg in ("-j", "--json"):
            json_flag = True
        elif current_arg in ("-s", "--summary"):
            full_flag = True
        elif current_arg in ("-h", "--help"):
            print_usage()

    if json_flag and full_flag:
        print("Can't output both json output and summary output simultaneously.")
        sys.exit(1)

    if values:
        input_file = values[0]
        if len(values) > 1:
            print("Error: Too many arguments provided.")
            sys.exit(1)

except getopt.error as err:
    print(str(err))


try:
    input_file
except NameError:
    print("Error: No input file given.")
    print_usage()
    sys.exit(1)
else:
    file_path = f"./{input_file}"

ip_stats = {}
packet_summaries = []
capture = pyshark.FileCapture(file_path)

try:
    for packet in capture:
        frame_number = packet.number
        timestamp = packet.sniff_time
        protocol = packet.highest_layer if hasattr(packet, 'highest_layer') else "Unknown"
        src_ip = packet.ip.src if 'IP' in packet else packet.eth.src
        dst_ip = packet.ip.dst if 'IP' in packet else packet.eth.dst
        length = int(packet.length)

        packet_summary = PacketSummary(frame_number, timestamp, protocol, src_ip, dst_ip, length)
        packet_summaries.append(packet_summary)

        if src_ip not in ip_stats:
            ip_stats[src_ip] = {
                "total_bytes_sent": 0,
                "common_destinations": Counter(),
                "protocols_used": Counter(),
                "active_hours": set()
            }

        ip_stats[src_ip]["total_bytes_sent"] += length
        ip_stats[src_ip]["common_destinations"][dst_ip] += 1
        ip_stats[src_ip]["protocols_used"][protocol] += 1
        ip_stats[src_ip]["active_hours"].add(timestamp.hour)

finally:
    capture.close()

for src_ip, stats in ip_stats.items():
    total_protocols = sum(stats["protocols_used"].values())
    protocol_percentages = {protocol: (count / total_protocols * 100) for protocol, count in stats["protocols_used"].items()}

    ip_stats[src_ip]["protocols_used"] = {protocol: f"{percentage:.2f}%" for protocol, percentage in protocol_percentages.items()}
    ip_stats[src_ip]["common_destinations"] = [dst_ip for dst_ip, _ in stats["common_destinations"].most_common(5)]
    ip_stats[src_ip]["active_hours"] = sorted(stats["active_hours"])

# Export to JSON before printing
if json_flag:
    for src_ip, stats in ip_stats.items():
        print(json.dumps(stats))


# Print report of all items
if full_flag:
    print("\nIP Statistics Report:")
    for src_ip, stats in ip_stats.items():
        print(f"\n{src_ip}:")
        print(f"  Total Bytes Sent: {stats['total_bytes_sent']}")
        print(f"  Common Destinations: {stats['common_destinations']}")
        print(f"  Protocols Used: {stats['protocols_used']}")
        print(f"  Active Hours: {stats['active_hours']}")

