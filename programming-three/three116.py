#!/usr/bin/python
# *-*coding:utf-8 *-*


"""
three 116page 当前工作路径CWD

当前工作路径CWD在脚本执行中是一个非常重要的概念。除非指定了绝对路径
否则当脚本处理文件时将始终默认它们存在于CWD。
谨记，没有完整目录路径的文件名将被映射到CWD路径，和你的PYTHONPATH设置无关
从技术上讲，一个脚本总是启动于CWD，而非它所在的目录。反之，import永远首先
搜索文件所在目录而非CWD（除非该脚本刚好在CWD）

CWD是你键入命令时所处的路径。另一方方面python自动将脚本所在目录添加到
模块搜索路径最前

脚本中没有目录路径的文件名将被映射到输入命令的地方os.getcwd，而通过
sys.path列表的首项，import总是可以看到当前正在运行脚本的路径

splitlines()按照换行符('\r','\r\n', '\n')分隔， 返回一个包含各行作为元素的列表
如果参数keepends为False返回值不包括换行符，如果为True则保留

Python isalpha() 方法检测字符串是否只由字母组成。返回bool值
Python isdigit() 方法检测字符串是否只由数字组成。返回bool值

"""


import sys
import os
import getopt
print(os.getcwd()) #当前工作路径
print(sys.path[:6])
print(sys.argv[1]) #获取命令行输入的启动参数
print(os.path.abspath('test1.py'))
print(getopt.getopt(sys.argv[1:]), 'hp:i', ["help","ip=","port="])
#print(os.environ)#获取运行它的shell(或父程序)中命令的变量


