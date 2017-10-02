#!/usr/bin/python
# *-*coding:utf-8 *-*

# 启动程序的其他方法.os.spawn函数
#一个跨平台的程序启动框架

"""
示例5-35 spawnv.py page=263
启动10个并行运行的child.py副本;在windows下用spawnv启动程序(类似
fork/exec组合);使用P_OBERLAY则进行替换，使用P_DETACH则子进程stdout
不指向任何地方;现在也可以使用可移植的subprocess或multiprocessing模块来完成

不自动退出
~$ python3 ~/py1/test13.py
Main process exiting
~$ Hello from child 5535 0
Hello from child 5536 1

"""
 
import os, sys

for i in range(10):
	if sys.platform[:3] == 'lin':
		pypath = sys.executable
		os.spawnv(os.P_NOWAIT, pypath, ('python3', '/home/asu/py1/test12.py', str(i)))
	else:
		pid = os.fork()
		if pid != 0:
			print('Process %d spawned' % pid)
		else:
			os.execlp("python3", 'python3', '/home/asu/py1/test12.py', str(i))

print('Main process exiting')


--------------------------------------------------------
#!/usr/bin/python
# *-*coding:utf-8 *-*


#一个跨平台的程序启动框架
"""
示例5-36 launchmodes.py page=267
#####################################################################
用命令行和可复用的启动方案类来启动Python程序;在命令行开有自动向Python可执行
文件插入"python"和/或路径;着模块的某些部分可能假定'python'在你的系统路径中

使用subprocess模块也可行，不过os.popen()在内部调用这个模块，目标是在这里启动一个独立
运行的程序，而非连接到它的流;mltiprocessing模块也是一个选择，不过这里处理命令而非函数，
为实现这里的选项之一而开始一个进程不是很合理;

这一版的更新：脚本文件名路径将经过normpath()处理，必要时将所有/改成\以供windows工具
使用;PyEdit和其他工具继承这个修正;在Windows下，一般允许在文件打开中用/，但并非所有启动工具
#############################################################################

"""

import os, sys

pyfile = (sys.platform[:3] == 'lin' and '/usr/bin/python') or 'python'
pyPATH = sys.executable #使用较新的pys中的sys

def fixWindowsPath(cmdline):
	"""
	将cmdline开头的脚本文件名路径里所有的/改成\;在windows下仅为运行需要这种
	处理的工具的类所使用;在其他平台上，这么做也没有坏处(笔图Linux下的os.system)
	"""
	splitline = cmdline.lstrip().split(' ') #在空格处分隔字符串
	fixePATH = os.path.normpath(splitline[0]) #解决斜杠的问题
	return ' '.join([fixePATH] + splitline[1:])

class LaunchMode:
	"""
	在实例中待命，声明标签并运行命令;子类按照run()中的需要格式化的命令行;
	命令应当以准备运行的Python脚本名开头，而且不带'Python'或脚本的完整路径
	"""

	def __init__(self, label, command):
		self.what = label
		self.where = command
	
	#__call__可以然个类的实例的行为表现的像函数一样
	def __call__(self): #等待调用，执行按钮按下的回调动作
		self.announce(self.what)
		self.run(self.where) #子类必须重新定义run
	
	def announce(self,text): #子类可以重新定义announce
		print(text)
	def run(self, cmdline):
		assert False, 'run must be defined'

class System(LaunchMode):
	"""
	运行shell命令行中指定的Python脚本，小心:可能阻塞调用者，
	除非在Unix下带上&操作符
	"""
	def run(self, cmdline):
		cmdline = fixWindowsPath(cmdline)
		os.system('%s %s' % (pyPATH, cmdline))

class Popen(LaunchMode):
	"""
	在新的进程中运行shell命令行; 注意：可能阻塞调用者，因为管道关闭的太快
	"""
	def run(self, cmdline):
		cmdline = fixWindowsPath(cmdline)
		os.popen(pyPATH+' '+ cmdline) #假设没有数据可取

class Fork(LaunchMode):
	"""
	在显示地创建的新进程中运行命令， 仅在类Unix系统下可用
	"""
	def run(self, cmdline):
		assert hasattr(os, 'fork')
		cmdline = cmdline.split() #把字符串转换成列表
		if os.fork() == 0:       #开始新的子进程， 在子进程中运行新程序
			os.execvp(pyPATH, [pyfile] + cmdline)
		
class Start(LaunchMode):
	"""
	独立于调用者运行程序;仅在Windows下可用：使用了文件名关联
	"""
	def run(self, cmdline):
		assert sys.platform[:3] == 'win'
		cmdline = fixWindowsPath(cmdline)
		os.startfile(cmdline)

class StartArgs(LaunchMode):
	"""
	仅在Windwos下可用：args可能需要用到真正的start命令;斜杠在这里没问题
	"""
	def run(self, cmdline):
		assert sys.platform[:3] == 'win'
		os.system('start' + cmdline) #可能会创建新弹出窗口

class Spawn(LaunchMode):
	"""
	在独立于调用者的新进程中运行Python;在windows和Unix下都可用;
	DOS中使用P——NOWAIT;斜杠在这里没问题
	"""
	def run(self, cmdline):
		os.spawnv(os.p_DETACH, pyPATH, (pyfile, cmdline))

class Top_level(LaunchMode):
	"""
	在新的窗口中运行， 进程是同一个;待讨论：还需要GUI类信息
	"""
	def run(self, cmdline):
		assert False, 'Sorry - mode not yet implemented'

#
#为这个平台挑选一个“最佳”启动器
#可能需要在其他地方细化这个选项
#

if sys.platform[:3] == 'win':
	PortableLauncher = Spawn
else:
	PortableLauncher = Fork

class QuitePortableLauncher(PortableLauncher):
	def announce(self, text):
		pass

def selftest():
	file = '/home/asu/py1/test15.py'
	input('default mode...')
	launcher = PortableLauncher(file, file)
	launcher() #不阻塞

	input('system mode ...')
	System(file, file)() #阻塞
	
	if sys.platform[:3] == 'win':
		input('DOS start mode ...')
		StartArgs(file, file)()

if __name__ == '__main__':
	selftest()



