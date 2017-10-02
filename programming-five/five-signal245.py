#!/usr/bin/python
# *-*coding:utf-8 *-*

#信号
#signal模块：https://docs.python.org/3/library/signal.html

"""
signal.signal (signalnum, handler) 
将信号signalnum的处理程序设置为handler。处理程序可以是一个可调用的Python对象，
它使用两个参数 信号编号和函数对象，布置该函数为此信号抛出时的处理器

signal.pause()
使进程休眠，直到捕捉下一个信号;然后将调用相应的处理程序。不返回任何值。

示例5-27 signal.py page=245
在python中捕获信号;将信号编号N作为命令行参数传入，利用shell命令 'kill -N pid'
向这个进程发送信号;大多数信号处理器在捕获信号后转到python中处理(关于SIGCHLD的细节
请参考“网络脚本”这一章);signal模块在windows下可用，不过仅定义了少数几
种信号类型，而且没有os.kill
"""

import sys, signal, time

def now():
	return time.ctime(time.time()) #当前时间字符串

def onSignal(signum, stackframe): #python信号处理器
	print('Go signal', signum, 'at', now())	 #多数信号处理器一直有效

signum = int(sys.argv[1])
signal.signal(signum, onSignal) #布置信号处理器
while True: #等待信号(或pass)
	signal.pause()

#运行 $ python signal1.py 12 & (12 信号编号 ，shell操作符& 指定在后台运行)
#$ kill -12 8224

----------------------------------------------------------


#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
signal.alarm(time)
如果时间不为零, 则此函数请求在时间秒内将SIGALRM信号发送到进程。
示例5-28 signal2.py page=246
在python中设置和捕获定时暂停信号，time.sleep和定时(或者在我的Linux-Pc上
的一般信号操作) 合用效果不好，所以我们在这里调用signal.pause来暂停操作，
直到接收到信号
"""

import sys, signal, time

def now():
	return time.asctime()

def onSignal(signum, stackframe): #python信号处理程序
	print('Got alarm', signum, 'at', now())

while True:
	print('Setting at', now())
	signal.signal(signal.SIGALRM, onSignal)	#设置信号处理器
	signal.alarm(5) #5秒后发送信号
	signal.pause() #等待信号


