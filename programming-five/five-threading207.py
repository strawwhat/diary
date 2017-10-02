#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
page = 207
给出了派生同类线程的4种不同方法

如果没有重新定义，Thread类的默认run方法直接调用传给其构造器的target参数
的调用对象，其参数为任意传给arg(默认为(),代表空)的参数。
这一点可以使得我们可以用Thread运行简单的函数，虽然这种调用形式并不比
基本的_thread模块中的做法简单多少
"""


import threading, _thread


def action(i):
	print(i**32)

#带有状态的子类
class Mythread(threading.Thread):
	def __init__(self, i):
		self.i = i
		threading.Thread.__init__(self)
	def run(self):
		print(self.i **32)

Mythread(2).start() #start方法调用run()


#传入行为
thread = threading.Thread(target=(lambda:action(2))) #run调用target
thread.start()

#同上，但是没有lambda函数将状态封装起来
threading.Thread(target=action, args=(2,)).start() #可调用对象及其参数


#基本线程模块
_thread.start_new_thread(action, (2,))



"""
Fatal Python error: could not acquire lock for <_io.BufferedWriter name='<stdout>'> at interpreter shutdown, possibly due to daemon threads

Thread 0x00007f84466b4700 (most recent call first):
  File "/home/asu/py1/test2.py", line 10 in action

Current thread 0x00007f8448970700 (most recent call first):
已放弃 (核心已转储)

=====================
第一次运行出现这个错误
关于这个错误介绍的两个博客
http://blog.csdn.net/VictoriaW/article/details/60579251
http://blog.sina.com.cn/s/blog_75bf554501019cvt.html
"""
------------------------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*

"""
面向对象编程(Object Oriented Programming,面向对象程序设计)是一种计算机编程架构。
OOP的一条基本原则是计算机程序是由单个能起到子程序作用的单元或对象组而成


有时会出现下列错误：
Fatal Python error: could not acquire lock for <_io.BufferedWriter name='<stdout>'> at interpreter shutdown, possibly due to daemon threads

Current thread 0x00007fdc23b46700 (most recent call first):
已放弃 (核心已转储)

"""

import threading, _thread


#线程类不一定得是Thread的子类
class Power:
	def __init__(self, i):
		self.i = i
	def action(self):
		print(self.i ** 32)

obj = Power(2)
threading.Thread(target=obj.action).start() #线程运行绑定方法

#利用嵌套作用域保留状态
def action(i):
	def power():
		print(i **32)
	return power
threading.Thread(target=action(2)).start() #线程运行返回的函数


#用基本线程模块实现二者
_thread.start_new_thread(obj.action, ())
_thread.start_new_thread(action(2), ())



