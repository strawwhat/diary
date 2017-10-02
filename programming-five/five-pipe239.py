#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
在某些平台上可以创建一个作为文件系统里真实的命名文件而存在的长时运行的管道。
这种文件称为具名管道。有时称为FIFO

命名管道由os.mkFIFO调用创建
在子进程中用os.open打开FIFO以获得底层的字节字符串访问权，但是在
父进程中则用内建函数open打开，将管道数据作为文本来处理。
任意一端可以使用任意技巧来处理管道数据，字节也好，文本也行。

因为FIFO与你的计算机上的一个真实的文件相关联，对于任何程序来说它们都是外部文件，
它们不依赖于任务间共享的内存，所以它们可以用作线程，进程及独立启动的程序间的IPC机制

os.mkfifo(path, mode=0o666, *, dir_fd=None)
以数字模式创建名为path的FIFO(命名管道)


示例5-24 pipefifo.py page=239
命名管道;os.mkfifo在windows下不能用，这里没有分支的必要，
因为fifo文件管道对于进程为外部文件--父进程/子进程中共享
文件描述符在这里没有效果
"""

import os, time, sys

fifoname = 'result.txt' #必须打开同名文件

def child():
	pipeout = os.open(fifoname, os.O_WRONLY) #作为文件描述符打开fifo
	zzz = 0
	while True:
		time.sleep(zzz)
		msg = ('Spam %03d\n' % zzz).encode()
		#os,True(pipeout, msg)
		os.write(pipeout, msg)
		zzz = (zzz+1) % 5

def parent():
	pipein = open(fifoname, 'r') #作为文本文件对象打开fifo
	while True:
		line = pipein.readline()[:-1] #数据发送完之前保持阻塞
		time.sleep(1)
		print('Parent %d got "%s" at %s' % (os.getpid(), line, time.time()))


#os.exists(path)  测试路径是否存在，返回False或True
if __name__ == '__main__':
	if not os.path.exists(fifoname):
		os.mkfifo(fifoname) #创建一个具名管道文件
	if len(sys.argv) == 1:  #如果没有参数则作为父进程运行，否则作为子进程
		parent()
	else:
		child()

