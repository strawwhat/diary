#!/usr/bin/python
# *-*coding:utf-8 *-*

"示例3-9 page134 redirect.py 重定向流到python对象"

"""
file-like objects that save standard output in a string and provide
standard input text a string ; redirect runs a passed-in function
with its output and input streams reset to these file-like class objects

类似文件的对象，用于在字符串中保存标准输出并提供
标准输入文本字符串; 重定向运行传入函数
其输出和输入流重新设置为这些类似文件的类对象

在Python中，任何在方法上与文件类似的对象都可以充当标准流。
它和对象数据类型无关，而取决于接口（有时被称为协议）即：

任何提供了类似于文件read方法的对象可以指定给sys.stdin，
以从该对象的read方法读取输入

任何定义了类似于文件write方法的对象可以指定给sys.stdout,
所有的标准输出将发送到该对象方法上
"""

import sys

class Output: 			#模拟输出文件
	def __init__(self):
		self.text = ''		#新建空字符串
	
	def write(self, string):
		self.text += string #添加字节字符串

	def writelines(self, lines): #在列表中添加每一行数据
		for line in lines: self.write(line) 

#模拟输入文件
class Input:
	def __init__(self, input=''): #默认参数
		self.text = input
	
	def read(self, size=None):  	#保存新建字符串,可选参数
		if size == None:			#读取n个字节，或者所有字节
			res, self.text = self.text, ''
		else:
			res, self.text = self.text[:size], self.text[size:]
		return res

	def readline(self):
		eoln = self.text.find('\n') #查找下一个eoln的偏移位置
		if eoln == -1: 				#清洗eoln,其值为-1
			res, self.text = self.text, ''
		else:
			res, self.text = self.text[:eoln+1], self.text[eoln+1:]
		return res
	

def redirect(function, pargs, kargs, input): #重定向stdin/out
	savestreams = sys.stdin, sys.stdout 	#运行函数对象
	sys.stdin = Input(input)				#返回stdout文件
	sys.stdout = Output()
	try:
		result = function(*pargs, **kargs)	#运行带参数的函数
		output = sys.stdout.text
		
	finally:
		sys.stdin, sys.stdout = savestreams  #如果存在exc或者其他，重新存储数据
	return (result, output)					#如果不存在exc，返回结束



