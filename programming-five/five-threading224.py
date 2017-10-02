#!/usr/bin/python
# *-*coding:utf-8 *-*

#进程的退出状态和共享状态
"""
示例5-17 testexit_fork.py page-224

分支子进程，用os.wait观察其退出状态;请注意：
派生线程共享全局变量，但每个分支进程拥有自己的全局变量副本
(分支共享文件描述符)。exitstat在这里将保持不变，而如果是线程
的话将发生变化

os.wait()
等待子进程完成，并返回包含其pid和退出状态的元组：
包含一个16位数字，其低字节是杀死进程的信号号，高字节是退出状态.
退出状态被包装进返回值的特定比特位置;它的确在那里，但我们需要
将结果右移8比特才能读出它
"""

import os
exitstat = 0


"""
分支进程作为其创建者的副本而开始运行，它们也拥有全局内存副本，
因此，每个分支进程获得并更改自己那份exitstat全局变量，
而不能更改其他进程的同一变量的副本。
"""
def child():       #在这里可以对脚本调用os.exit
	global exitstat #更改这个进程的全局变量
	exitstat += 1   #发送到父进程的wait函数的退出状态
	print('Hello from child', os.getpid(), exitstat)
	os._exit(exitstat)
	print('never reached')

def parent():
	while True:
		newpid = os.fork()  #开始进程的新副本
		if newpid == 0:    #如果是在副本中，那么运行子程序的逻辑业务
			child()
		else:
			pid, status = os.wait()
			print('Parent got', pid, status, (status >> 8))
			if input() == 'q':
				break

if __name__ == '__main__':
	parent()
------------------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

#线程的退出和共享状态
#线程在同一进程里并行运行并共享全局内存
"""
示例5-8 testexit_thread.py
派生线程来观察共享全局内存的变化;线程通常在其运行的函数返回时退出，
但可以调用_thread.exit结束其调用的线程，_thread.exit和sys.exit相同，
也会抛出SystemExit异常;线程与可能被锁定的全局变量进行通信;
在某些平台上可能需要做单元的打印/输入调用--stdout是共享的

_thread.get_ident() 
返回当前线程的‘线程标识符’。这是一个非零整数。
它的价值没有直接意义;它的目的是作为一个神奇的 cookie, 
用于索引一个线程特定的数据字典。当线程退出时, 
线程标识符可能被回收, 并且创建另一个线程。

_thread.exit()
引发 SystemExit 异常。当未被捕获时, 这将导致线程退出静默。

"""

import _thread
exitstat = 0

def child():
	global exitstat #进程中的全局名称为所有线程共享
	exitstat +=1
	threadid = _thread.get_ident()
	print('Hello from child', threadid, exitstat)
	_thread.exit()
	print('never reached')

def parent():
	while True:
		_thread.start_new_thread(child, ())
		if input() == 'q': break

if __name__ == '__main__':
	parent()
	
	

	
	
	

			
	
