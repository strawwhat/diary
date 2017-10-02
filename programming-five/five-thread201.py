#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例5-8 thread-count-wait.py page-201
使用全局锁列表来探知所有子线程的结束时间 使用mutexes 在父/主线程中探知线程何时结束，
而不再使用time.sleep;给stdout加锁以避免混杂在一起的打印

主线程为每个子线程创建一把锁并将其加入全局列表exitmutexes,
(线程中的函数和主线程共享全局作用域)。退出时每个线程获取
列表中的锁，而主线程仅仅关注所有锁被获取
"""

import _thread
stdoutmutex = _thread.allocate_lock()
exitmutexes  = [_thread.allocate_lock() for i in range(10)]
exitmutex = [False] *10

def counter(myId, count):
    for i in range(count):
        stdoutmutex.acquire()
        print('[%s] => %s' % (myId, i))
        stdoutmutex.release()
    #exitmutexes[myId].acquire() #向主线程发送信号
    exitmutex[myId] = True

#创建的子线程和要全局锁列表数量一致，否则while死循环
for i in range(10):
    _thread.start_new_thread(counter, (i, 5))

#lock.locked()返回锁状态：如果锁已被某个线程获取则为True，否则为False
#for mutex in exitmutexes:
    #while not mutex.locked(): pass
while False in exitmutex: pass
print("Main thread exiting.")

---------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
with语句可以用来确保在一段嵌套代码块周围执行线程操作，线程锁的上下文
管理器在with语句这一行获取锁，然后语句结束时释放锁，实际效果不仅节省了一行代码，
而且确保在可能出现异常的情况下，锁仍然得到释放。


示例5-10 thread-coun-wait3.py page-203

传入所有线程共享的mutex对象而非所有全局对象;
和上下文管理器语句一起使用，实现锁的自动获取/释放;
添加休眠功能的调用以避免繁忙的循环并模拟真实工作
"""


import _thread, time

stdoutmutex = _thread.allocate_lock() #输出锁对象
numthreads = 5
exitmutexes = [_thread.allocate_lock() for i in range(numthreads)] #全局锁对象列表

#将锁作为参数而非在全局作用域中引用，这会使传入线程中的函数可能更加一致
def counter(myId, count, mutex): #传入共享对象
	for i in range(count):
		time.sleep(1 / (myId + 1)) #每个线程的不同休眠时长
		with mutex:
			print("[%s] => %s" % (myId, i))
	exitmutexes[myId].acquire()

for i in range(numthreads):
	_thread.start_new_thread(counter, (i, 5, stdoutmutex))

# all()函数用于判定给定的可迭代参数iterable中的所有元素
#是否不为 0、''、False或者iterable为空，如果是返回True，否则返回False
while not all(mutex.locked() for mutex in exitmutexes): time.sleep(0.25)
print('Main thread end!')




