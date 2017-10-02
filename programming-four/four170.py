#!/usr/bin/python
# *-*coding:utf-8 *-*

"""filters.py 文件过滤器 page-170"""

import sys

#显式指定文件
def filter_file(name, function):
	input = open(name, 'r')  #通过函数筛选文件
	output = open(name + '.out', 'w')  #创建文件对象
	for line in input:
		output.write(function(line))  #写入修改后的行
	input.close()
	output.close()

#用标准输入输出流来允许在命令行中重定向
def filter_stream(function):    #不显式指定文件
    while True:
        line = sys.stdin.readline()  #使用标准输入流，或者input
        if not line: break
        #print(function(line), end='') #或者者使用：sys.stdout.write()
        sys.stdout.write(function(line))

if __name__ == '__main__':
	from test5 import processLine
	#filter_stream(lambda line: line)  #如果运行，则将stdin复制到stdout
	#filter_stream(processLine)

	filepath = sys.argv[1]
	filter_file(filepath, processLine)

----------------------------------------------------------
#上下文管理器
#如果执行处理的函数失败而抛出异常，文件能立即关闭
def filter_files(name, function):
    with open(name, 'r') as input, open(name + '.out', 'w') as output:
        try:
            for line in input:
                output.write(function(line))
        except Exception as e:
            print('Error: ', e)
#文件对象的行迭代简化基于流的过滤器的相应代码
def filter_stream(function):
    for line in sys.stdin:
        print(function(line), end='')

from test5 import processLine
import sys

filepath = sys.argv[1]

filter_files(filepath, processLine)


