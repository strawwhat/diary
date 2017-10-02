#!/usr/bin/python
# *-*coding:utf-8 *-*

#套接字基本操作
"""
文档：https://docs.python.org/3/library/socket.html

daemon()设置为子线程是否随主线程一起结束，默认为False，如果要随主线程一起结束需设置为True

#套接字用于跨任务通信：启动线程，相互通过套接字通信，也适用于独立程序，
因为套接字是系统级别的，类似FIFO;书中的GUI和Internet部分更有贴近实践套接字
用例，某些套接字服务器可能还需要与线程或进程中的客户端通信，套接字传输字节
字符串，后者可以是pickle后的对象或编码后的Unicode文本;注意，如果线程中打印输出
可能重叠的话，则仍然需要同步化操作

示例5-25 socket_preview.py page=241
"""

from socket import socket, AF_INET, SOCK_STREAM #可移植的套接字API

port = 5008 #机器上套接字的端口号标识符
host = 'localhost' #在这里，服务器和客户端在同一台本地机器上运行

def server():
	sock = socket(AF_INET, SOCK_STREAM) #3个参数1地址族2流(默认)或数据报套接字3是使用协议
	sock.bind(('',port)) #tcp连接的ip地址 绑定到这台机器的端口上
	sock.listen(5) #允许最多五个等待中的客户端
	while True:
		conn, addr = sock.accept() #等待客户端连接
		data = conn.recv(1024) #从这个客户端读取字节数据
		reply = 'server got: [%s]' % data #conn是一个新连接上的套接字
		conn.send(reply.encode())  #将字节华的回复发回客户端

def client(name):
	sock = socket(AF_INET, SOCK_STREAM) #连接一个套接字端口
	sock.connect((host, port))
	sock.send(name.encode()) #向监听者发送数据
	reply = sock.recv(1024) #从监听者那里接收字节数据
	sock.close()
	print('client got : [%s]' % reply)

if __name__ == '__main__':
	from threading import Thread
	sthread = Thread(target=server)
	sthread.daemon = True
	sthread.start()
	for i in range(5):
		Thread(target=client, args=('client%s' % i,)).start()

-------------------------------------------------------------------------------

#!/usr/bin/python
# *-*coding:utf-8 *-*

#套接字和独立程序
"""
示例 5-26 socket-preview-progs.py page=243
同样的套接字，除了在线程间通信，还在独立程序间通信;此处的服务器在
进程中运行，为线程和进程中的客户端提供服务;套接字是机器水平的全局
对象，类似fifo，无须内存共享
"""

from test1 import server, client #二者使用相同的端口号
import sys, os
from threading import Thread

mode = int(sys.argv[1])
if mode == 1:
	server()
elif mode == 2:
	client('client:process=%s' % os.getpid())
else:
	for i in range(5):
		Thread(target=client, args=('client:thread=%s' % i,)).start()


