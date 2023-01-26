"""
IPV4 header structure
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  0|Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 32|         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 64|  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 96|                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
128|                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
160|                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

SRC rfc791
"""

from ctypes import *
import socket
import struct

class IPC(Structure):
    _fields_ = [
            ("ihl",              c_ubyte,     4),     # 4 bits unsigned char
            ("ver",          c_ubyte,     4),     # 4 bits unsigned char
            ("tos",              c_ubyte,     8),     # 1 byte unsigned char
            ("len",              c_ushort,   16),     # 2 bytes unsigned short 
            ("id",               c_ushort,   16),     # 2 bytes unsigned short
            ("offset",           c_ushort,   12),     # 12 bits unsigned short
            ("flags",            c_ushort,    4),     # 4 bits unsigned short 
            ("ttl",              c_ubyte,     8),     # 1 byte unsigned char
            ("protocol_num",     c_ubyte,     8),     # 1 byte unsigned char
            ("sum",              c_ushort,   16),     # 2 bytes unsigned short 
            ("src",              c_uint32,   32),     # 4 bytes unsigned int 
            ("dst",              c_uint32,   32),     # 4 bytes unsigned char
            ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print("%s No protocol for %s" % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

