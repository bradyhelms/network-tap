import pyshark
from collections import defaultdict, Counter

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

fp = './example_pcap.pcapng'

protocol_counts = Counter()
total_packet_length = 0
source_ip_counts = Counter()

packet_summaries = []

cap = pyshark.FileCapture(fp)

try:
    for packet in cap:
        frame_number = packet.number
        timestamp = packet.sniff_time
        protocol = packet.highest_layer if hasattr(packet, 'highest_layer') else "Unknown"
        src_ip = packet.ip.src if 'IP' in packet else packet.eth.src
        dst_ip = packet.ip.dst if 'IP' in packet else packet.eth.dst
        length = int(packet.length)

        packet_summary = PacketSummary(frame_number, timestamp, protocol, src_ip, dst_ip, length)

        packet_summaries.append(packet_summary)

        protocol_counts[protocol] += 1
        total_packet_length += length
        source_ip_counts[src_ip] += 1

finally:
    cap.close()

#print("\nPacket Summaries:")
#for summary in packet_summaries:
#    print(summary)

print("\nStatistics:")
print("\nProtocol Counts:")
for protocol, count in protocol_counts.items():
    print(f"  {protocol}: {count}")

print(f"\nTotal Packet Length: {total_packet_length} bytes")

print("\nTop 5 Source IPs:")
for ip, count in source_ip_counts.most_common(5):
    print(f"  {ip}: {count} packets")

