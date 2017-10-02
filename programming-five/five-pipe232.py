#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例5-21 pipe-thread.py page-232
#匿名管道和线程而非进程，这个版本可以在window上工作
"""
import os, time, threading

def child(pipeout):
	zzz = 0
	while True:
		time.sleep(zzz)
		msg = ('Spam [%s]' % zzz).encode()
		os.write(pipeout, msg)
		zzz = (zzz + 1) % 5

def parent(pipein):
	while True:
		line = os.read(pipein, 32)
		print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

pipein, pipeout = os.pipe()
threading.Thread(target=child, args=(pipeout,)).start()
parent(pipein)
