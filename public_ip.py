#!/usr/bin/env python
# coding: utf-8
import array
import sys
import socket
import time
import struct
import os
import select
if sys.platform.startswith("win32"):
    default_timer = time.clock
else:
    default_timer = time.time
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
    return socket.gethostbyaddr(addr)
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
        self.timeout = timeout
        self.reached = False
    def run(self):
        ttl_num = 1
        while not self.reached:
            self.getip(ttl_num)
            ttl_num += 1
    def getip(self,ttl_num):
        self.send_one_icmp(ttl_num)
    def send_one_icmp(self,ttl_num):
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname('icmp'))
        checksum = 0
        header = struct.pack('!BBHHH',ICMP_ECHO,0,checksum,s
def main():
    pass
if __name__=='__main__':
    main()
