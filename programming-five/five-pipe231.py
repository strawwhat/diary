#!/usr/bin/python
# *-*coding:utf-8 *-*

#把管道描述符封装进文件对象,然后通过该文件对象的readline方法在管道中搜索下一个\n分隔符号

"""
示例5-20 pipe2.py page-231
和pipe1.py一样不过将管道输入封装金stdio文件对象
在两个进程中逐行读取并关闭管道文件描述符


os.fdopen(fd, *args, **kwargs)
返回连接到文件描述符fd的打开的文件对象。这是 open()内置函数的别名, 并接受相同的参数。
os.fbopen()默认r文本模式，这个版本的读取操作返回一个文本数据str对象
"""


import os, time

def child(pipeout):
	zzz = 0
	while True:
		time.sleep(zzz) #让父进程等待
		msg = ('Spam %03d\n' % zzz).encode() #管道在3.x中是二进制的
		os.write(pipeout, msg) #发送到父进程
		zzz = (zzz+1) % 5

def parent():
	pipein, pipeout = os.pipe() #创建带有两个末端的管道
	if os.fork() == 0:
		os.close(pipein) #关闭输入端
		child(pipeout) #在子进程中写入
	else:
		os.close(pipeout) #关闭输出端
		pipein = os.fdopen(pipein) #创建文本模式的输入文件对象
		while True:
			line = pipein.readline()[:-1]  #数据发送完之前保持阻塞
			print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

parent()



