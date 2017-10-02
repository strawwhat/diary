#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
遍历目录树 os.walk访问器
lister_walk.py page178

os.walk() 从操作上来看os.walk是一个生成器函数，在树的每个目录中
它产生一个包含三个项目的元组，包括 当前目录的名称，所有子目录组成的列表，
当前目录下所有文件组成的列表。

了解os.walk()到底是如何工作的，只需手动调用几次它的__next__方法，
或者使用内建函数next()，就像for循环自动进行那样；每次调用时
你都会前进到目录树中的下一个子目录

"""

import sys, os


def lister(root): #对于根目录
	for (thisdir, subshere, fileshere) in os.walk(root): #生成目录树的目录列表
		print('[' + thisdir + ']')
		for fname in fileshere:		#打印这个目录下的文件
			path = os.path.join(thisdir, fname)
			print(path)

if __name__ == '__main__':
	lister(sys.argv[1]) #目录名从命令行传入

----------------------------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
page 178
循环遍历每一级目录的所有文件，寻找以.py结尾并且包含搜索字符的文件
"""

import os
def match(directory, filetype, matches):
	result = []
	for (dirname, dirshere, fileshere) in os.walk(directory):
		for filename in fileshere:
			if filename.endswith(filetype):
				pathname = os.path.join(dirname, filename)
				if matches in open(pathname).read():
					result.append(pathname)
	return result

if __name__ == '__main__':
	print(match('/home/asu/py1/', '.py', 'os.walk'))

-----------------------------------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
#以递归的方式列举目录树中的文件
os.walk()另一种实现方式
page 180
"""

import sys, os

def mylister(currdir):
	print('[-' + currdir + '-]')
	for file in os.listdir(currdir):
		path = os.path.join(currdir, file)
		if not os.path.isdir(path):
			print('|     |',path)
		else:
			mylister(path)

if __name__ == '__main__':
	mylister(sys.argv[1])




