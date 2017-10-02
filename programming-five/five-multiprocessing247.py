#!/usr/bin/python
# *-*coding:utf-8 *-*


#基本操作进程和锁 page =249
#multiprocessing模块：https://docs.python.org/3.5/library/multiprocessing.html
"""
介绍博客：http://www.cnblogs.com/kaituorensheng/p/4445418.html
Lock() 创建一个共享的threading.Lock对象并返回一个代理。
class multiprocessing.Process(group=None, target=None, name=None, 
args=(), kwargs={}, *, daemon=None)
进程对象表示在单独进程中运行的活动。进程类具有所有线程处理方法的等效threading.Thread.



multiprocessing使用进程而非线程来并行的运行代码，所以它有效的避开了线程的GIL带来的限制

multiprocessing模块基本操作：Process功能类似threading.Thread，不过在并行
进程而非线程中运行函数调用;可以用锁进行同步化，如某些平台上的打印操作;
在windows下启动新的解释器，在Unix下分支新进程

"""

import os
from multiprocessing import Process, Lock

def whoami(label ,lock):
	msg = "%s: name:%s, pid:%s"
	with lock:
		print(msg % (label, __name__, os.getpid()))

if __name__ == '__main__':
	lock = Lock()
	whoami('function all', lock)
	
	p = Process(target=whoami, args=('spawned child', lock))
	p.start()
	p.join()
	
	for i in range(5):
		p = Process(target=whoami, args=(('run process %s' % i), lock)).start()

	with lock:
		print('Main process exit')

----------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

# multiprocessing模块的管道
"""
示例5-30 nulti2.py page=253
使用多进程匿名管道进行通信，返回两个connnection对象来分别代表管道的两端，
对象从另一端发送，在另一端接收，不过管道默认是双向的

Pipe()函数返回一对由管道连接的连接对象，默认情况下是双工(双向)
每个连接对象都有send()和recv()方法(等等)
"""

import os
from multiprocessing import Process, Pipe

def sender(pipe):
	'''在匿名管道上向父进程发送对象'''
	pipe.send(['spam'] + [42, 'eggs'])
	pipe.close()

def talker(pipe):
	'''通过管道发送和接收对象'''
	pipe.send(dict(name='Bob', spam=42))
	reply = pipe.recv()
	print('talker got:', reply)

if __name__ == '__main__':
	(parentEnd, childEnd) = Pipe()
	Process(target=sender, args=(childEnd,)).start() #派生带有管道的子进程
	print('parent got:', parentEnd.recv()) #从子进程处接收
	parentEnd.close() #或者在全局目录中自动关闭

	(parentEnd, childEnd) = Pipe()
	child = Process(target=talker, args=(childEnd,))
	child.start()
	print('parent got:', parentEnd.recv()) #从子进程处接收
	parentEnd.send({x*2 for x in 'spam'}) #向子进程发送
	child.join() #主进程阻塞，等待子进程退出。守护进程就是不阻挡主程序退出，自己干自己的
	print('parent exit')

---------------------------------------------------------

#!/usr/bin/python
# *-*coding:utf-8 *-*

#共享内存和全局对象
"""
示例5-31 multi3.py page==254 将共享内存作为进程的输入和输出
使用多进程共享内存对象进行通信。传输的对象是共享的，但在windows下
不共享全局对象，这里最后那个测试代表了通常的用例：分配工作。

multiprocessing.Value(typecode_or_type, *args, lock=True)
返回从共享内存分配的ctypes对象。

multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
返回从共享内存分配的ctypes数组。
"""

import os
from multiprocessing import Process, Value, Array

procs = 3 #每个进程各自的全局全局对象，并非共享
count = 0

def showdata(label, val, arr):
	'''在这个进程中打印数据值'''
	msg = '%-12s: pid:%4s, global:%s, value:%s, array:%s'
	print(msg % (label, os.getpid(), count, val.value, list(arr)))

def updater(val, arr):
	'''通过共享内存进行通信'''
	global count #全局计数器
	count += 1
	val.value += 1 #传入的对象是共享的
	for i in range(3): arr[i] += 1

if __name__ == '__main__':
	scalar = Value('i', 0) #共享内存是进程/线程安全的
	vector = Array('d', procs) #ctypes中的类型代码:就像int和double
	
	#在父进程中显示起始值
	showdata('parent start', scalar, vector)
	
	#派生子进程，传入共享内存
	p = Process(target=showdata, args=('child', scalar, vector))
	p.start(); p.join()

	# 传入父进程中更新过的共享内存，等待每次传入结束
	#每个子进程看到了父进程中到现在为止对args的更新(但全局变量的看不到)
	
	print('\nloop1 (updataes in parent, serial children)...')
	for i in range(procs):
		count += 1
		scalar.value += 1
		vector[i] += 1
		p = Process(target=showdata, args=(('process %s' % i), scalar, vector))
		p.start(); p.join()
	
	#同上，不过允许子进程并行运行
	#所有进程都看到了最近一次迭代的结果，因为它们都共享这个对象
	print('\nloop2 (updates in parent, parallel children)...')
	ps = []
	for i in range(procs):
		count += 1
		scalar.value += 1
		vector[i] += 1
		p = Process(target=showdata, args=(('Process %s' % i), scalar, vector))
		p.start()
		ps.append(p)
	for p in ps: p.join()

	#共享内存在派生子进程中进行更新，等待每个更新结束
	print('\nloop3 (updates in serial children)...')
	for i in range(procs):
		p = Process(target=updater, args=(scalar, vector))
		p.start()
		p.join()
	showdata('parent temp', scalar, vector)

	#同上，不过允许子进程并行地进行更新
	ps = []
	print('/nloop4 (updates in parallel cildren)...')
	for i in range(procs):
		p = Process(target=updater, args=(scalar, vector))
		p.start()
		ps.append(p)
	for p in ps: p.join()
#仅在父进程中全局变量count=6

#在此显示最终结果                       #scalar=12; 父进程中+6,6个子进程中均+6
	showdata('parent end', scalar, vector) #array[i]=8; 父进程中+2,6个子进程均+2


---------------------------------------------------------------------

#!/usr/bin/python
# *-*coding:utf-8 *-*

#队列和子类
"""
class multiprocessing.Queue ([maxsize])
使用管道和几个锁/信号灯实现的进程共享队列。
put (obj [, block [, timeout]]) 将obj放入队列中。
get ([block [, timeout]]) 从队列中移除并返回项。
block为False, 如果一个项可用,则立即返回该项, 
队列是空将引发队列 queue.Empty()异常

示例5-32 multi4.py page=256
可以创建Process类的子类，就像threading.Thread一样;Queue和queue.Queue
的使用方法类似，不过它不是线程间的工具，而是进程间的工具
"""

import os, time, queue
from multiprocessing import Process, Queue
#进程安全的共享队列，队列是管道+锁/信号机

class Counter(Process):
	label = ' @'
	def __init__(self, start, queue): #为运行中的用处保留状态
		self.state = start
		self.post = queue
		Process.__init__(self)

	def run(self): #新进程中调用start()使开始运行
		for i in range(3):
			time.sleep(1)
			self.state += 1
			print(self.label, self.pid, self.state) #self.pid为该子进程的pid
			self.post.put([self.pid, self.state]) #stdout文件为所有进程共享
		print(self.label, self.pid, '-')

if __name__ == '__main__':
	print('start', os.getpid())
	expected = 9

	post = Queue() 
	p = Counter(0, post) #开始共享队列的3个进程
	q = Counter(100, post) #子进程是个生产者
	r = Counter(1000, post)
	p.start(); q.start(); r.start()

#父进程消耗队列中的数据 从本质上来说，这就像一个GUI，虽然GUI使用线程
	while expected:  
		time.sleep(0.5)
		try:
			data = post.get(block=False)
		except queue.Empty:
			print('no data...')
		else:
			print('posted:', data)
			expected -= 1

	p.join(); q.join(); r.join() #必须在join putt之前进行
	print('finish', os.getpid(), r.exitcode)

------------------------------------------------------


#!/usr/bin/python
# *-*coding:utf-8 *-*s

"""
示例5-33 multi5.py page=258
使用multiprocessing起始新程序，不论os.fork是否可用
"""
import os, time
from multiprocessing import Process

def runprogram(arg):
	os.execlp('python3', 'python3', '/home/asu/py1/test10.py', str(arg))

if __name__ == '__main__':
	for i in range(5):
		Process(target=runprogram, args=(i,)).start()
	print('parent exit')
-------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例5-34 multi6.py page=259
演示multiprocessing对pool(协同完成一个给定任务的一组派生子进程)的支持
"""

import os
from multiprocessing import Pool


def powers(x):
	#print(os.getpid()) #能够监视子进程
	return 2 ** x

if __name__ == '__main__':
	#维持执行的进程总数为processes，当一个进程执行完后会添加新的进程进去
	workers = Pool(processes=5)
	results = workers.map(powers, [2]*100)
	print(results[:16])
	print(results[-2:])
	
	results = workers.map(powers, range(100))
	print(results[:16])
	print(results[-2:])


