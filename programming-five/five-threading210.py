#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
queu模块 https://docs.python.org/3/library/queue.html

queue.Queue(maxsize=0)
FIFO队列的构造函数。maxsize是一个整数，用于设置可以放置在队列中项目数量的上限。
一旦达到此大小，将阻止插入直到使用队列项。如果maxsize小于或等于零，则队列大小为无穷大。

Queue.put(item, block=True, timeout=None) 将项目放入队列中。
如果可选参数block是True，并且timeout是None(默认)，
则在必要时阻止，直到有空闲slot可用。如果超时是正数, 则它会在大多数超时秒内阻塞,
如果没有空闲slot, 则会引发完全异常。否则(block为False)，如果空闲slot立即可用，则将项目
放在队列中，否则会引发完全异常。

Queue.get(block=True, timeout=None) 从队列中移除并返回项
如果可选的参数块是True, 并且超时是None(默认), 则在必要时阻止, 直到有可用的项为止。
如果超时是正数, 则它会在大多数超时秒内阻塞, 如果在该时间之内没有可用的项, 则会引发空异常。
否则 (block为false), 如果一个项目立即可用, 则返回该项, 否则引发空异常 (在这种情况下忽略超时)

exception queue.Empty
当在空的队列对象上调用非阻塞get()(或get_nowait())时引发异常。


示例5-14 queuetes.py page=210
生产者和消费者线程与共享队列进行通信

注意队列是如何给一个全局变量赋值的。因为这一点，它可以在所有派生的线程中
共享(他们是在同一进程，同一作用域下运行)。因为这些线程改变对象而非变脸名，
所以将队列作为参数传入线程的函数也是可行的。

"""

numconsumers = 2 #准备开始的消费者线程数目
numproducers = 4 #准备开始的产生者线程的数目
nummessages = 4 #每个生产者存入的消息的数量

import _thread, queue, time

safeprint = _thread.allocate_lock() #否则打印操作可能发生重叠
dataQueue = queue.Queue() #共享的全局变量，大小无限

def producer(idnum):
	for msgnum in range(nummessages):
		time.sleep(idnum)
		dataQueue.put('[producer id=%d, count=%d]' % (idnum, msgnum)) #向队列中加入项

def consumer(idnum):
	while True:
		time.sleep(0.1)
		try:
			data = dataQueue.get(block=False)#从队列中删除并返回项
		except queue.Empty:
			#print('queue.Empty')
			pass
		else:
			with safeprint:
				print('consumer', idnum, 'got =>', data)


if __name__ == '__main__':
	for i in range(numconsumers):
		_thread.start_new_thread(consumer, (i,))
	
	for i in range(numproducers):
		_thread.start_new_thread(producer, (i,))
	
	#注意脚本是如何随其主线程而退出的，即使消费者线程仍在其无限循环中运行。
	#使用基本的_thread模块时，程序在其主线程退出后安静的退出，这就是需要休眠的原因
	#需要为线程提供完成工作的时间
	time.sleep(((numproducers-1) * nummessages) + 1)#避免主线程过早退出
	print('Main thread exit')

#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例5-14的threading版本 page=212
在theading模块中，如果任何一个派生线程仍在运行中，程序不会退出，
除非那些线程被设定为守护线程。具体来说，整个程序仅在只剩下守护线程的情况下才会退出

threading.Thread().daemon = True/False
守护进程
一个布尔值，指示此线程是否为守护线程（True）或否（False。
这必须在start（）被调用之前设置，否则引发RuntimeError。
它的初始值是从创建线程继承的; 主线程不是一个守护线程，
因此在主线程中创建的所有线程都默认为daemon = False。
"""



import threading, queue, time

numconsumer = 2
numproduct = 4
nummessage = 4

dataQueue = queue.Queue()
safeprint = threading.Lock()

def product(idnum, dataQueue):
	for msgnum in range(numproduct):
		time.sleep(idnum)
		dataQueue.put('[product id=%s, count=%s]' % (idnum, msgnum))

def consumer(idnum, dataQueue):
	while True:
		time.sleep(0.1)
		try:
			data = dataQueue.get(block=False)
		except queue.Empty:
			pass
		else:
			with safeprint:
				print('consumer %s => %s' % (idnum, data))


if __name__ == '__main__':
	for i in range(numconsumer):
		thread = threading.Thread(target=consumer, args=(i, dataQueue))
		thread.daemon = True
		thread.start()

	waitfor = []
	for i in range(numproduct):
		thread = threading.Thread(target=product, args=(i,dataQueue))
		waitfor.append(thread)
		thread.start()

	for thread in waitfor: thread.join() #或者在这里执行一个足够长的time.sleep()
	print('Main thread exit')



