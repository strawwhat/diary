#!/usr/bin/env python
# *-*coding:utf-8 *-*

"""
shell环境变量

shell变量有时称之为环境变量，python脚本可以通过一个类似python字典的对象os.environ来访问它们
在该对象里每项(entry 条目)对应一个shell变量设置

"""


"""
标准流 page124
sys模块提供了 python的标准输入，标准输出和错误流，它们是又一通用的程序通信方式

标准流是预先打开的python文件对象，它们在python启动时自动连接到你的程序上。
标准流默认在python(或python程序)启动时被绑定到控制台窗口
内部的print和input函数实际上只是标准输入/输出流的接口

重定向流到文件或程序
重定向对于预编码测试输入等非常有用：每次脚本启动时，通过重定向标准输入流到不同的文件，
可以将一个测试脚本应用于任意的输入
重定向标准输出流使得我们能够保存以及后续分析一个程序的输出

可以利用shell语法 '< filename' 把标准输入流重定向到文件输入
标准输出 shell语法 '> filename' 重定向到文件中

管道操作 在windows和类Unix平台上，在两个命令之间设用shell字符'|', 
可以将一个程序的标准输出发送到另一个程序的标准输入。
由于shell创建了连接两个命令输入和输出的管道，通常称为管道操作

"""

import sys
#示例3-5 page125 
"read numbers till eof and show squares"

def interact():
	print('Hello stream world')
	while True:
		try:
			reply = input('Enter a number>')
		except EOFError:
			break
		else:
			num = float(reply) # int(reply)
			print("{0} squared is {1}".format(num, num**2)) #format格式会保存小数的平方
			#print("%d squared is %d" %(num, num**2))
			#sys.stdout.write('%d squared is %d\n' % (num, num**2))
	print('Bye')

if __name__ == '__main__':
	interact()

