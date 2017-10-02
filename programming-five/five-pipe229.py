#!/usr/bin/python
# *-*coding:utf-8 *-*

#匿名管道：匿名管道的基本操作
"""
管道是单向的同道，有点像共享内存的缓冲，但对于其两端来接口说类似于
一个简单的文件。通常的用法是，一个程序在管道的一端写入数据，而另一个程序
在另一端读取数据。
对于管道的读取调用总是返回最先写入管道的数据，导致一个先进先出的模型--
最先写入的数据是最先读出的。

分支后，原始的父进程及其子进程副本在分支前os.pipe()创建的管道两端进行流。
os.pipe()调用返回一个包含两个文件描述符的元组，这两个文件描述符代表着
这根管道的输入端和输出端。

因为分支出来的子进程复制其父进程的文件描述符，所以子进程中向管道输出描述符
的写入可以将数据发回管道的父进程，而这些管道是在子进程派生之前就已经创建好的。



示例5-19 pipe1.py page-229
os.read(fd, n) 从文件描述符fd读取最多n个字节。返回包含读取的字节的bytestring。
os.write(fd, str)将str中的bytestring写入文件描述符fd。返回实际写入的字节数。
"""

import os, time

def child(pipeout):
	zzz = 0
	while True:
		time.sleep(zzz) #让父进程等待
		msg = ('Spam %03d' % zzz).encode() #管道是二进制字节，所以编码
		os.write(pipeout, msg) #发送到父进程
		zzz = (zzz+1) % 5

def parent():
	pipein, pipeout = os.pipe() #创建带有两个末端的管道
	if os.fork() == 0:
		child(pipeout)
	else:
		while True: #一个字=2字节(1 word=2byte),1字节=8位(1byte=8bit). msg是8个byte。把zzz注释掉
			line = os.read(pipein, 32)
			print('parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

parent()

