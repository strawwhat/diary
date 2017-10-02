#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
我们看到了线程中的打印操作需要用锁进行同步以避免重叠，
这是因为输出流是在所有线程间共享的。
更加正式的说法是，线程需要通过它们对任何可能在同一进程中
的线程间共享项(对象和命名空间)的更改进行同步化。
根据给定的程序的目的，这些对象可能包括：
内存中的可变对象、全局作用域中的名称、模块中的内容

示例5-12 thread-add-random.py page-208
在win7下运行时打印不同的结果，ubuntu是同样的结果
"""
import threading, time

count = 0

def adder():
	global count
	count = count +1 #更新全局作用域中一个共享的名称，线程共享对象内存及全局名称
	time.sleep(0.5)
	count = count + 1

threads =[]
for i in range(100):
	thread = threading.Thread(target=adder, args=())
	thread.start()
	threads.append(thread)

for thread in threads: thread.join()
print(count)

---------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
示例-5-13 thread-add-synch.py page=209
每次都打印200,因为共享资源访问已经同步化
"""

import threading, time

count = 0

def adder(addlock): #传入共享锁对象
	global count
	with addlock:
		count += 1
	time.sleep(0.5)
	with addlock:
		count += 1

addlock = threading.Lock()
threads = []

for i in range(100):
	thread = threading.Thread(target=adder, args=(addlock,))
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()

print(count)

