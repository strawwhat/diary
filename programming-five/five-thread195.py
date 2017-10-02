#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
线程
文档：https://docs.python.org/3/library/_thread.html

线程是在同一时间内启动其他操作的另一种方法。简单来说，它们和程序的其他部分
并行的调用函数(或者其他可调用的对象类型)。线程有时被称为“轻量级进程“，
因为他们向分支进程一样并行运行，但是所有线程均在用一个进程中运行。
进程通常用来起始独立的程序，而线程经常用于非阻塞的输入调用和GUI中
长时间运行的任务。

"""

"""
#示例5-5 thread1.py page195
_thread.start_new_thread(function, args[, kwargs])
启动一个新的线程并返回其标识符。线程使用参数args（它必须是元组）执行函数。
可选的kwags参数指定关键子参数的字典。当函数返回时，线程静默的退出
如果线程中的函数抛出未捕获的异常，则打印堆栈跟踪记录并退出线程，
但程序的其他部分继续运行

"""

import _thread

def child(tid):
	print('Hello from thread', tid)
	print(1/0)

def parent():
	i = 0
	while True:
		i += 1
		_thread.start_new_thread(child, (i,))
		if input() == 'q': break

parent()

----------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*


"""
page 197
绑定方法在这里尤其有用，因为它们能记住方法的函数和实例对象，
它们还能够访问线程运行过程中 其内部的状态信息及类方法的访问权限。
更为根本的是，因为所有线程都在同一进程中运行，线程中的绑定方法引用那个 
在进程中原始的实例对象，而非它的副本
"""

import _thread

def action(i):
	print(i**64)

class Power():
	def __init__(self, i):
		self.i = i
	def action(self):
		print(self.i ** 64)

_thread.start_new_thread(action, (2,))
_thread.start_new_thread((lambda: action(2)), ())

obj = Power(2)
_thread.start_new_thread(obj.action, (2,))

-----------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

#示例5-6 thread_count.py page197

"""
线程基本操作：并行的启用5个函数副本，利用time.sleep避免主线程
过早退出，这样在某些系统平台上将导致其他线程中止，共享stdout：
线程输出在这个版本里可能随机混合在一起
任何子线程还在运行的时候 主线程退出了 所有派生的子线程会立即终止
这一点和进程不一样
"""

import _thread
import time

def counter(Myid, count):
	for i in range(count):
		time.sleep(1)
		print('[%s] => %s' % (Myid, i))

for i in range(5): #派生5个子线程，每个线程循环5次
	_thread.start_new_thread(counter, (i, 5))
time.sleep(6)#避免过早退出
print('Main thread exiting')

