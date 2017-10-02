#!/usr/bin/python
# *-*coding:utf-8 *-*

#用匿名管道进行双向IPC
"""
示例5-22 pipes.py page=233
派生一个子进程/程序，连接我的stdin/stdout和子进程的stdin/stdout,
我的读写映射到派生程序的输出和输入上;很像利用subprocess模块绑定流一样
示例中的spaw函数分出一个新的子程序并将父程序的输入和输出流连接到子程序的输入和输出流

当父程序自其标准输入读取时，它在向子程标准输出的文本
当父程序对其标准输出写入时，它在向子程序的标准输出发送数据

这里的os.dup2()是最根本的函数。例如,os.dup2(parentStdin, stdinFd)这个调用
将父进程的管道输入端赋值给stdin，所有stdin从此开始从管道读取

os.close(fd) 关闭文件描述符
os.dup2(fd, fd2, inheritable=True)
把文件描述符fd命名的文件所有相关的系统信息复制到由fd2命名的文件中

"""

import os, sys

def spawn(prog, *args): #传入程序名称
    stdinFd = sys.stdin.fileno() #厚的流的描述符
    stdoutFd = sys.stdout.fileno() #一般stdin=0,stdout=1

    parentStdin, childStdout = os.pipe() #创建两个IPC管道频道
    childStdin, parentStdout = os.pipe() #pipe返回(输入流文件描述符，输出流文件描述符)
    pid = os.fork()
    if pid:
        os.close(childStdout) #分支之后，在父进程中
        os.close(childStdin) #在父进程中关闭子进程端
        os.dup2(parentStdin, stdinFd) #我的sys.stdin副本赋值为pipe1[0]
        os.dup2(parentStdout, stdoutFd) #我的sys.stdout副本赋值为pipe2[1]
    else:
        os.close(parentStdin) #分支后，在子进程中
        os.close(parentStdout) #在子进程中关闭父进程端
        os.dup2(childStdin, stdinFd) #我的sys.stdin副本赋值为pipe2[0]
        os.dup2(childStdout,stdoutFd) #我的sys.stdout副本赋值为pipe1[1]
        args = (prog,) + args
        os.execvp(prog, args) #这个进程中的新程序
        assert False, 'exevp failed' #不让os.exec调用返回法哦这里

if __name__ == '__main__':
        mypid = os.getpid()
        spawn('python', '/home/asu/py1/test14.py', 'spam') #分支子程序

        print(b'Hello 1 from parent %d' % mypid) #发送到子进程的stdin
        sys.stdout.flush() #清理stdio缓冲区
        reply = input()  #发到子进程的stdout
        sys.stderr.write('Parent got: "%s"\n' % reply)

        print(b'Hello 2 from parent %d ' % mypid)
        sys.stdout.flush()
        reply = sys.stdin.readline()
        sys.stderr.write('Parent got: "%s"\n' % reply[:-1])

---------------------------------------------------------------------------
"""
示例5-23 pipes-testchild.py page=235
为了测试5-22
sys.stderr()解释器用于标准输入、输出和错误的文件对象
""" 
import os, time, sys

mypid = os.getpid()
parentpid = os.getppid()
#注意如果两个程序要显示消息的话需要向stderr写入，它们的stdout流已经连接了其他程序的输入流
#因为进程共享文件描述符，stderr在父进程和子进程中相同，所以状态消息在同一个地方显示
sys.stderr.write('Child %d of %d got arg: "%s"\n' % (mypid, parentpid, sys.argv[1]))

for i in range(2):
    time.sleep(3)  #通过这里的休眠让父进程等待
    recv = input() #stdin绑定到管道上，来自父进程的stdout
    time.sleep(3)
    send = 'Child %d got: [%s]' % (mypid, recv)
    print(send) #stdout绑定到管道上，发至父进程的stdin
    sys.stdout.flush() #确保数据已经发送，否则阻塞进程

