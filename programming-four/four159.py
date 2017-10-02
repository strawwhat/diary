#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
page -159
struct 模块提供用于打包和解压二进制数据的调用
它能够用你想用的任何一种字节序来进行组合和分解
（字节序决定了二进制数字的最高位是居左还是居右）

文档链接:https://docs.python.org/3/library/struct.html
"""

import struct
import binascii

values = (1, 'abc', 2.7)
s = struct.Struct('I3sf')

packed_data = s.pack(*values) #打包
unpacked_data = s.unpack(packed_data) #解包

print(values)
print(s.format)
print(s.size)
print(binascii.hexlify(packed_data))
print(type(unpacked_data), unpacked_data)

---------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*'

import struct 

data = struct.pack('>I4sIf', 2, b'spam', 3, 1.234)

print(data)

file = open('temp.bin', 'wb')
file.write(data)
file.close()


files =open('temp.bin', 'rb')
bytes = files.read()
print(bytes)
values = struct.unpack('>I4sIf', data)
print(values)


