#!/usr/bin/python
# *-*coding:utf-8 *-*

"示例3-8 page130 moreplus.py 重定向流和用户交互"


"""
split and interactively page a string, file, or stream of
text to stdout; when run as a script, page stdin or file 
whose name is passed on cmdline; if input is stdin, can't
use it for user reply--use platform-specific tools or GUI

python File isatty()方法
概述 isatty()检测文件是否连接到一个终端设备，如果是返回True，否则返回False
语法 fileobject.isatty() 无参数

windows中的控制台工具msvcrt
ubuntu中类似的模块 getch
https://stackoverflow.com/questions/38172907/msvcrt-module-equivalent-on-ubuntu
https://pypi.python.org/pypi/getch
"""

import sys


def getreply():
	"""
	读取交互式用户回复键，即使stdin重定向到到某个文件或者管道
	"""
	
	if sys.stdin.isatty(): #如果stdin是控制台，从stdin读取回复行数据
		return input('?')
	else:
		#if sys.platform[:3] == 'win': #如果stdin重定向不能用于询问用户
		if sys.platform == 'linux':
		
			#import msvcrt 				#使用windows控制台工具，getch()方法不能回应键
			#msvcrt.putch(b'?')
			#key = msvcrt.getche()
			#msvcrt.putch(b'\n')
			key = open('/dev/tty').readline()[:-1]
			return key
		else:
			assert False, 'platform not supported'

def more(text, numline=15):
	"""
	page multiline string to srdout
	"""
	lines = text.splitlines()
	while lines:
		chunk = lines[:numline]
		lines = lines[numline:]
		for line in chunk: print(line)
		if lines and getreply() not in ['y', 'Y']: break

#流重定向时没有返回？号, 给命令行参数时运行正确
if __name__ == '__main__':
	if len(sys.argv) == 1: 			#运行时比较，而不是导入时比较
		more(sys.stdin.read())		#如果不存在命令行参数，在stdin页没有输入数据
	else:
		more(open(sys.argv[1]).read())



