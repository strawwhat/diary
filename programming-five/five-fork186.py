#!/usr/bin/python
# *-*coding:utf-8 *-*


"""
示例5-1 fork1.py page186

os.fork()

https://docs.python.org/3/library/os.html

python中的fork()函数可以获得系统中进程的PID(Process ID)，
返回0则为子进程，否则就是父进程。
子进程永远返回0,而父进程返回子进程ID。这样做的理由是一个父进程可以fork()
出很多子进程，所以父进程要记下每个子进程的ID，而子进程只需要调用getpid()就可以拿到父进程的ID

os._exit()类似于sys.exit()，但它不执行任何的清除工作(例如刷新缓冲区)。
所以os._exit()尤其适用于退出子进程。如果程序使用sys.exit()，
操作系统会回收父进程或其它子进程可能仍然需要的资源。
传给os._exit()函数的参数必须是进程的退出状态。退出状态为0，表示正常终止。


1.fork()调用后会创建一个新的子进程,这个子进程是原父进程的副本.子进程可以独立父进程外运行.
2.fork()是一个很特殊的方法,一次调用,两次返回.
3.fork()它会返回2个值,一个值为0,表示在子进程返回;另外一个值为非0,表示在父进程中返回子进程ID.
"""
#×××os.fork()创建的子进程会接着下一行代码继续执行×××
#分支出子进程，直到你输入 'q'

import os

def child():
	print("Hello from child", os.getpid())
	os._exit(0) #否则将回到父循环中


def parent():
	while True:
		newpid = os.fork()
		if newpid == 0:
			child()
		else:
			print("Hello from parent", os.getpid(), newpid)
		if input == 'q': break

parent()

