#!/usr/bin/env pytohn3

import argparse
from scapy.all import *


def read_pkt(pcap_file):
    packet = rdpcap(pcap_file)

    data = b''
    counter = 0
    missing_pkt = []
    for i in range(len(packet)):
        if packet[i]['IP'].src == '192.168.131.1' and len(packet[i]) > 1000:

            counter += 1
            
            load = packet[i]['Raw'].load


            if int.from_bytes(load[24:26],'big') != counter:
                print('jump')
                for j in range(counter,int.from_bytes(load[24:26],'big')):
                    print("%d %x is missing" % (j,j))
                    missing_pkt.append(j)
                
            print(int.from_bytes(load[24:26],'big'))
            counter = int.from_bytes(load[24:26],'big')
            data += load[28:]
            

    print(missing_pkt)
    return data
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="snmptrapgen", add_help=True)
    parser.add_argument("-f", "--file", type=str,
                        required=True, help="Specify .pcap file.")
    parser.add_argument("-d", "--dst_ip", type=str,
                        required=False, help="Sepcify destination ip address.")
    parser.add_argument("-s", "--src_ip", type=str,
                        required=False, help="Specify source ip address.p")
    args = parser.parse_args()

    data = read_pkt(args.file)

    f = open('./stora.7z','wb')
    f.write(data)
    f.close
