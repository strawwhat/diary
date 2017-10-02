#!/usr/bin/python
# *-*coding:utf-8 *-*


"""文件扫描器 page169"""


#经验性原则，一般可以把使用Python程序进行的各种处理转交给内建工具，从而使程序提速
#scanner并不关心传入的行处理函数，而这成全了它的通用性--
#将任意已有或有待将来编写的单个参数函数应用于文本文件的所有行

"""
def sanner(name, function):
	for line in open(name, 'r'):
		function(line)
"""
def sanner(name, function):
	#list(map(function, open(name, 'r'))) #map函数
	#[function(line) for line in open(name, 'r')]  #列表解析表达式
	list(function(line) for line in open(name, 'r'))  #生成器解析表达式



from sys import argv

class UnknownCommand(Exception): pass


commands = {'*':'Ms.', '+':'Mr.'}
#简单的逐行转换的客户端脚本
def processLine(line):
	try:
		#print(commands[line[0]], line[1:-1])
		return commands[line[0]] + line[1:-1] + '\n' #在过滤器中使用
	except KeyError:
		pass
		#raise UnknownCommand(line)

"""
filename = 'data.txt'
if len(argv) == 2: filename = argv[1]
sanner(filename, processLine)
"""


