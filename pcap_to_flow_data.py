import dpkt
import json
import os
import socket


def parse_pcap_to_json(pcap_file):
    flows = {}
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for _, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                src_ip = socket.inet_ntoa(ip.src)
                dst_ip = socket.inet_ntoa(ip.dst)
                bytes_transferred = len(buf)

                # Check if the IP packet contains TCP/UDP to get the ports
                if isinstance(ip.data, (dpkt.tcp.TCP, dpkt.udp.UDP)):
                    transport = ip.data
                    src_port = transport.sport
                    dst_port = transport.dport
                else:
                    src_port = None
                    dst_port = None

                # Use a tuple (src_ip, dst_ip, src_port, dst_port) as the key for the flows dictionary
                flow_key = (src_ip, dst_ip, src_port, dst_port)
                if flow_key in flows:
                    flows[flow_key]["bytes_transferred"] += bytes_transferred
                else:
                    flows[flow_key] = {
                        "source_ip": src_ip,
                        "destination_ip": dst_ip,
                        "source_port": src_port,
                        "destination_port": dst_port,
                        "bytes_transferred": bytes_transferred
                    }

    return {"flows": list(flows.values())}


if __name__ == "__main__":
    pcap_file = "172-16-100-54-whats-app-video-call-sara.pcap"  # Replace with your pcap file path
    data = parse_pcap_to_json(pcap_file)

    # Save the data to a JSON file with the same name as the pcap file
    json_file = os.path.splitext(pcap_file)[0] + ".json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data saved to {json_file}")
