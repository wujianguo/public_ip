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
        pass
def main():
    pass
if __name__=='__main__':
    main()
