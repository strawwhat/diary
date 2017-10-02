#!/usr/bin/python
# *-*coding:utf-8 *-*'

"""
three 118page 解析命令行参数

python可以通过sys模块获取脚本启动时命令行输入的信息，通常它们被称为
命令行参数，以字符串列表的形式存在于sys.argv中

一个惯例，类似function参数，命令行参数通过位置或使用 '-name value'词组来传递.
例如 -i data.txt表示-i对应的值为data.txt，任何词都可以显示，单程序通常将他们结构化

短选项模式(-)和长选项模式(--)
"""


#解析命令行参数 实例3-2


def getopts(argv):
	opts = {}
	while argv:
		if argv[0][0] == '-':
			opts[argv[0]] = argv[1]
			argv = argv[2:]
		else:
			argv = argv[1:]
	return opts


if __name__ == '__main__':
	import sys
	myargvs = getopts(sys.argv)
	if '-i' in myargvs:
		print(myargvs['-i'], '-i')
	print(myargvs)



