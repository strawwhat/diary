#/usr/bin/env python
# *-*coding:utf-8 *-*

#python 3 爬取赵雷歌词

from collections import Counter
from urllib import request
from bs4 import BeautifulSoup as BS
import jieba
import os 

songlists = ['http://www.xiami.com/album/465009', 'http://www.xiami.com/album/2100205356', 'http://www.xiami.com/album/2013969781', 'http://www.xiami.com/album/2102413795']
songlist  = 'http://www.xiami.com/album/465009'
writefile = '~/Downlaod/赵雷歌词.txt'


class xiamimusic():
	
	def __init__(self):
		self.zhaolei = open(writefile, 'w')
		self.weburl ='http://www.xiami.com'

	def get_html(self,urll):
		webheaders = {  'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
		req = request.Request(url= urll, headers= webheaders)
		html = request.urlopen(req).read().decode('utf-8')
		return html


	def get_lyrics_html(self,urll):

		soup = BS(self.get_html(urll), 'html.parser')
		for tdtag in soup.find_all('td', class_="song_name"):
			for line in tdtag.find_all('a'):
				if len(line.get('href')) > 10:
					songurl = os.path.join(self.weburl + line.get('href'))

					soup = BS(self.get_html(songurl), 'html.parser')
					for divtag in soup.find_all('div', class_= 'lrc_main'):
						#song_words = set(jieba.cut(divtag.get_text(), cut_all= False))
						self.zhaolei.write(divtag.get_text())
		self.zhaolei.close()

		

s = xiamimusic()
s.get_lyrics_html(songlist)


