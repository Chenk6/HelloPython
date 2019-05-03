import requests
import json
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

def handle_href(title, a_herf):
	#创建一个参数对象，用来控制chrome以无界面模式打开
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	#驱动路径
	path = r'E:\Users\tool\chromedriver.exe'
	#创建浏览器对象
	browser = webdriver.Chrome(executable_path=path,chrome_options = chrome_options)
	browser.get(a_herf)
	time.sleep(3)
	# 获取源码，生成tree对象，然后查找video里面的src属性
	tree = etree.HTML(browser.page_source)
	#找到视频的url
	video_src = tree.xpath('//video[@tabindex = "2"]/@src')[0]
	video_src = 'http:' + video_src
	# print(video_src)
	# exit()
	#为视频创建一个存储目录
	dirname = 'shipin'
	path = r'E:\Users\day16'
	if not os.path.exists(dirname):
		os.mkdir(dirname)
	dirpath = os.path.join(path,dirname)
	filename = title + '.mp4'
	filepath = os.path.join(dirpath,filename)
	r = requests.get(video_src)
	print('%s开始下载...'%title)
	with open(filepath,'wb')as fp:
		fp.write(r.content)

	print('%s下载结束.'%title)
	# exit()

def handle_title():
	#捕获的接口url
	url = 'https://www.365yg.com/api/pc/hot_video/'
	r = requests.get(url, headers=headers)
	# print(r.text)
	#将json字符串转化为python对象
	obj = json.loads(r.text)
	data_list = obj['data']
	# 循环data列表，依次取出每一个视频的信息
	for data in data_list:
		#视频的url
		display_url = data['display_url']
		#视频的标题
		title = data['title']
		#拼接视频的url
		a_herf = 'http://www.365yg.com' + display_url
		#处理每一个视频url
		handle_href(title,a_herf)

def main():
	handle_title()

if __name__ == '__main__':
	main()