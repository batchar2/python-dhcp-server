#!/usr/bin/env python3

import ctypes


class DHCPDiscover(ctypes.LittleEndianStructure):
    _fields_ = [
        ('op', ctypes.c_uint8, 8),
        ('htype', ctypes.c_uint8, 8),
        ('hlen', ctypes.c_uint8, 8),
        ('hops', ctypes.c_uint8, 8),
        
        ('xid', ctypes.c_uint32, 32),

        ('secs', ctypes.c_uint16, 16),
        ('flags', ctypes.c_uint16, 16),

        ('ciaddr', ctypes.c_uint32, 32),

        ('yiaddr', ctypes.c_uint32, 32),


        ('siaddr', ctypes.c_uint32, 32),


        ('giaddr', ctypes.c_uint32, 32),


        ('chaddr', ctypes.c_uint32, 128),

        ('sname', ctypes.c_uint32, 512),


        ('file', ctypes.c_uint32, 1024),

        ('options', ctypes.c_uint32, 32),

    ]



if __name__ == '__main__':
    pass