#/usr/bin/python
# *-*coding:utf-8 *-*


"""
turtle 画火树银花

在此大婶文章内容上加颜色和修改角度长度
# http://www.bkjia.com/Pythonjc/847768.html  python实现绘制树枝简单示例

"""
import turtle as t
import random


colors = ['red', 'blue', 'green', 'yellow', 'pink', 'red', 'purple', 'crimson', 'orange', 'turquoise', 'navy']

longs = [ 0.7, 0.8, 0.9, 0.95]
angle = [15, 20, 25, 30]

t.bgcolor('black')
t.pencolor('green')
t.speed(12)

def branch(length, level):
	pen = random.choice(colors)
	t.pencolor(pen)
	lon = random.choice(longs)
	ang = random.choice(angle)
	if level <= 0:
		return 

	t.forward(length)
	t.left(ang)
	branch(lon * length, level -1)
	
	t.right(ang*2)
	
	branch(lon * length, level -1)
	t.left(ang)
	t.backward(length)
	
	return 

t.left(90)

def test():
	for i in range(80, 100):# 80, 100
		t.setheading(i)
		branch(100, 9)

	while True:
		s = input()
		if s:
			break

test()

"""
#/usr/bin/python
# *-*coding:utf-8 *-*

import turtle as t
import random




colors = ['red', 'blue', 'green', 'yellow', 'pink', 'red', 'purple', 'crimson', 'orange', 'turquoise', 'navy']

t.bgcolor('black')
t.pencolor('green')
t.speed(12)

def branch(length, level):
	pen = random.choice(colors)
	t.pencolor(pen)
	if level <= 0:
		return 

	t.forward(length)
	t.left(25)
	branch(0.8 * length, level -1)
	
	t.right(50)
	
	branch(0.8 * length, level -1)
	t.left(25)
	t.backward(length)
	
	return 

t.left(90)

def test():
	for i in range(80, 100):# 80, 100
		t.setheading(i)
		branch(100, 9)	
	while True:
		s = input()
		if s:
			break

test()
"""
