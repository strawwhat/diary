#!/usr/bin/python
# *-*coding:utf-8 *-*


"""
page-189
os.execl(program, cmdarg1, cmdarg2, …, cmdargN)
基本的”l”执行形式,需要传入可执行的程序名,以及用来运行程序的命令行多个字符参数.


os.execlp()的参数 通过指定即将运行程序的命令行参数来运行程序.(即python脚本中的sys.argv)
os.execlp调用可以用一个全新的程序代替(即执行覆盖)当前进程中正在运行的程序
由于这个原因, os.fork和os.execlp的组合意味着开始一个新的进程，并在其中
运行一个新的程序。换言之，启动与原有程序并行运行的新程序



"""


import os
import subprocess

parm = 0
while True:
	parm += 1
	pid = os.fork()
	if pid == 0:
		os.execlp('python', 'python', '/home/asu/py1/test5.py', str(parm))	# 复制进程，覆盖原来的程序
		assert False, 'error starting program'		#不应该返回
	else:
		print('Child is', pid)
		if input() == 'q': break


