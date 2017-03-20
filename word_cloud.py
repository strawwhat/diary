#/usr/bin/env python
# *-*coding:utf-8 *-*

#模块介绍https://amueller.github.io/word_cloud/
#python 3.5.2

from scipy.misc import imread
from wordcloud import WordCloud
import matplotlib.pyplot as plt


filepath = '~/Download/Janeeyre.txt'
picturepath = '~/Download/anne.png'
fontpath = '~/Download/simfang.ttf'

text = open(filepath, 'r').read()

back_picture = imread(picturepath)

#设置 字体 字体间距 背景色 最多词汇数量 词云形状 最大号字体 计算和图片之间的缩放
wc = WordCloud(font_path = fontpath,
				font_step = 3,
				background_color = 'black',
				max_words = 200,
				mask = back_picture,
				max_font_size = 100,
				random_state = 42,
				scale = 5
)

#生成词云
wc.generate(text)

#运行后显示图片
plt.figure()
plt.imshow(wc)
plt.axis('off')
plt.show()
#保存图片
wc.to_file( "Janeeyre.jpg")

'''-----------------------------------------------------------------------------------'''
#/usr/bin/env python
# *-*coding:utf-8 *-*


from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from collections import Counter

#读入文本

text = open('~/Download/西游记.txt').read()

#使用jieba# 分词
text_jieba = list(jieba.cut(text))
#使用 counter 做词频统计 选取出频率前100的词汇
c = Counter(text_jieba)
common_c = c.most_common(100)
#读取图片
bg_pic = imread('~/Download/anne.png')
#配置词云参数
wc = WordCloud(
	font_path = '~/Download/李旭科书法.ttf',
	#font_path = '/home/asu/py2/simfang.ttf',
	background_color = 'white',
	max_words = 2000,
	mask = bg_pic,
	max_font_size = 200,
)

#生成词云
wc.generate_from_frequencies(dict(common_c))
#生成图片显示
plt.figure()
plt.imshow(wc)
plt.axis('off')
plt.show()

wc.to_file('xi youji.jpg')


