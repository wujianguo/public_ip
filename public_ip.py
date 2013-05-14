#!/usr/bin/env python
# coding: utf-8
import array
import sys
import socket
import struct
import os
ICMP_PROTOCOL = 1
ICMP_ECHO = 8
ICMP_MAX_RECV = 2048
def is_valid_ipv4_address(addr):
    parts = addr.split('.')
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            if int(part) > 255:
                return False
        except:
            return False
    return True
def to_ip(addr):
    if is_valid_ipv4_address(addr):
        return addr
    return socket.gethostbyname(addr)
def calculate_checksum(source_string):
    if len(source_string)%2:
        source_string += "\x00"
    converted = array.array("H", source_string)
    if sys.byteorder == "big":
        converted.byteswap()
    val = sum(converted)
    val &= 0xffffffff
    val = (val >> 16) + (val & 0xffff)
    val += (val >>16)
    answer = ~val & 0xffff
    answer = socket.htons(answer)
    return answer
class traceroute():
    def __init__(self,destination, timeout=1000):
        self.destination = to_ip(destination)
        print("destination:%s"%self.destination)
        self.timeout = timeout
        self.own_id = os.getpid()
        self.packet_size = 55
        self.reached = False
    def header2dict(self, names, struct_format, data):
        """ unpack the raw received IP and ICMP header informations to a dict """
        unpacked_data = struct.unpack(struct_format, data)
        return dict(zip(names, unpacked_data))

    def run(self):
        ttl_num = 1
        while ttl_num<55:
            thisip = self.getip(ttl_num,35455)
            print(thisip)
            ttl_num += 1
    def getip(self,ttl_num,remote_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl_num)
#        sock.setsockopt(socket.IPPROTO_IP,socket.IP_RR,4,)
#        sock.setsockopt(socket.SOL_IP,0x07,4,)
        self.send_one_icmp(sock,ttl_num)
        return self.receive_one_icmp(sock)

    def send_one_icmp(self,sock,ttl_num):
        checksum = 0
        header = struct.pack('!BBHHH',ICMP_ECHO,0,checksum,self.own_id,self.packet_size)
        padBytes = []
        startVal = 0x42
        for i in range(startVal,startVal + (self.packet_size)):
            padBytes += [(i & 0xff)]
        data = bytes(padBytes)
        checksum = calculate_checksum(header + data)
        header = struct.pack('!BBHHH',ICMP_ECHO,0,checksum,self.own_id,self.packet_size)
        packet = header + data
#        print(data)
        sock.sendto(packet,(self.destination,1))
    def receive_one_icmp(self,sock):
        sock.settimeout(10)
        while True:
            try:
                packet_data, address = sock.recvfrom(ICMP_MAX_RECV)
            except:
                return None
            ip_header = self.header2dict(
                names=[
                    "version", "type", "length",
                    "id", "flags", "ttl", "protocol",
                    "checksum", "src_ip", "dest_ip"
                ],
                struct_format="!BBHHHBBHII",
                data=packet_data[:20]
                )
            ip_header_len = (ip_header['version'] & 0xf) * 4
#            print(packet_data[28:])
            icmp_header = self.header2dict(
                names=[
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format="!BBHHH",
                data=packet_data[ip_header_len:ip_header_len+8]
            )
            ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
            print(ip)
#            print(socket.inet_ntoa(struct.pack("!I", ip_header["dest_ip"])))
            return ip, ip_header, icmp_header

def main():
    t = traceroute("baidu.com")
    t.run()
if __name__=='__main__':
    main()
