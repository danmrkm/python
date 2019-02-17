from scapy.all import *

packet = rdpcap('./some.pcap')
output = b""

for pkt in packets:
    if (pkt['ICMP'].id == 0x5677) and (pkt['ICMP'].type == 8):
        output += pkt['Raw'].load[0x1c:]

fil = open("aaa.7z",'wb')
file.write(outpu)
file.close()
