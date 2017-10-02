#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例 5-2 fork-count.py page-187

分支进程基本操作：本程序启用了5个副本，与原有程序并行运行;
每个副本在同一个标准标准输出流上重复5次，分支操作复制进程内存，
包括文件描述符;目前分支操作在没有Cygwin和windows下不能运行，
在windows下可以用os.spawnv或者multiprocess来代替，spawnv大概
相当于fork和exec的组合
"""

import os, time

#子进程中运行的函数
def counter(count):
	for i in range(count):
		time.sleep(1)
		print('[%s] => %s' % (os.getpid(), i))


for i in range(5):
	pid = os.fork()
	if pid != 0:
		print("Process %d spwned" % pid) #在父进程中
	else:
		counter(5)	#否则在子进程中，运行函数并退出
		os._exit(0)

print("Main process exiting") #父进程不用等待



