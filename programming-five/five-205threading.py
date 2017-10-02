#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
threading 模块 https://docs.python.org/3/library/threading.html
python自带两个线程模块：_thread较低层面上的基本接口
thrading基于对象和类的较高层面的接口。threading模块在内部
使用_thread模块来实现代表线程的对象以及常用同步化工具的功能

threading.Thread()
start() 开始线程的活动。每个线程对象最多只能调用一次。
它为对象的的run()方法安排在单独的控制线程中调用。

run() 表示线程活动的方法。
你可以在子类中重写此方法。标准run()方法将调用传递给对象
构造函数的可调用对象作为目标参数(如果有),并分别从args和kwargs
实参中获得顺序和关键字参数

join(timeout=None)
等待线程终止。这将阻止调用线程，直到调用其join()方法的线程终止，
通常或通过未经处理的异常--或者直到可选的超时发生


class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
示例5-11 thread-class.py page205
带有状态和run()行为的线程类实例使用较高层面的上的Java的threading模块
对象连接方法(而非mutexes或共享全局变量)在主线程中探知线程结束时间
"""

import threading

#子类Thread对象
class Mythread(threading.Thread):
	def __init__(self, myId, count, mutex):
		#各线程状态信息，共享对象，不是全局对象
		self.myId = myId
		self.count = count
		self.mutex = mutex
		threading.Thread.__init__(self)
		#super().__init__()
	
#run函数启动线程后自动调用的方法。提供线程逻辑任务，仍然同步化stdout访问
	def run(self):
		for i in range(self.count):
			with self.mutex:
				print("[%s] => %s" % (self.myId, i))

#与thread.allocate_locak()相同,由_thread扩展模块实现
stdoutmutex = threading.Lock()
threads = []

#创建并开始10个线程，在线程中开始运行run方法
for i in range(10):
	thread = Mythread(i, 100, stdoutmutex)
	thread.start()
	threads.append(thread)

for thread in threads:
	#print(thread.is_alive())
	thread.join()#等待被调用的线程终止
print('Main thread end')


