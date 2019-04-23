import urllib.request
import urllib.parse
import json
import jsonpath
import re
import time

items_list = []


def handle_request(page):
	url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=577249277344&spuId=1058639181&sellerId=1917047079&order=3&'
	data = {
		'currentpage':page
	}
	querring_data = urllib.parse.urlencode(data)
	url = url + querring_data
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
		'Cookie': 'cna=wmhlFOeW2CMCAdxzF3FGJccJ; sm4=120000; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E4%B8%83%E5%B9%B4%E4%B9%8B%E7%BA%A6%E5%B0%8F%E4%B8%83; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=cm%2FOumxiXRpota94McsVjRpBebK9Ge%2F0xQ%2B4tYhLOYYxeb8qYtWimqaI9U4i1Q%2BucJZZCu5HcwHx5qWUUi%2Fp6g%3D%3D; uc1=cookie14=UoTZ4tN3fwF4Bw%3D%3D; t=ba301f8c0f0db6011745b9bea1c82b3c; uc3=vt3=F8dByEiTkKjp%2BrQ7nCs%3D&id2=UUGq2QhVdraVvw%3D%3D&nk2=pZ3Rq0RLwMAo2yHD&lg2=V32FPkk%2Fw0dUvg%3D%3D; tracknick=%5Cu4E03%5Cu5E74%5Cu4E4B%5Cu7EA6%5Cu5C0F%5Cu4E03; lgc=%5Cu4E03%5Cu5E74%5Cu4E4B%5Cu7EA6%5Cu5C0F%5Cu4E03; _tb_token_=e513b4eede13f; cookie2=7f58dcddf94ac492113d2bdbb391a271; _m_h5_tk=cb897b802b0fd6d23310b72911c9674e_1556014747348; _m_h5_tk_enc=0b71d809a5ca6a7815bf4724a967e68e; l=bBQZahDcv2dVDPbaBOfgmZZrN1QtPKOffPVPhN022IB19p5qOdI5KHwp0WHHU3Q_E_5HNeKz9Shd2REkWJzLRr1..; isg=BLGxfczWSf7-JOXLUCdLV7iywD1Bnr03_h4it5PPhX1iut4M2uyt4Occ3A55d71I'
	}
	req = urllib.request.Request(url=url, headers=headers)
	return req
def parse_json_text(json_text):
	json_text = re.sub(r'.*?\(', '', json_text)
	json_text = re.sub(r'\)', '', json_text)
	# print(type(json_text))
	obj = json.loads(json_text)  # 把json格式字符串转化为python对象
	# print(obj)
	ratelist = jsonpath.jsonpath(obj,'$.rateDetail.rateList[*]')
	#print(ratelist)
	for content in ratelist:
		name = jsonpath.jsonpath(content,'$.displayUserNick')[0]
		comment = jsonpath.jsonpath(content,'$.rateContent')[0]
		comment_date = jsonpath.jsonpath(content,'$.rateDate')[0]
		info = jsonpath.jsonpath(content,'$.auctionSku')[0]
		pic = jsonpath.jsonpath(content,'$..pics')[0]
		if len(pic)!= 0 :
			pics = 'https' + ''.join(pic)
		else:
			pics = ''
		#print(pics)
		#exit()
		item = {
			'用户名':name,
			'评论时间':comment_date,
			'评论':comment,
			'商品信息':info,
			'图片评论':pics
		}
		items_list.append(item)

	string = json.dumps(items_list,ensure_ascii=False)
	with open('taobao.txt','w',encoding='utf-8')as f:
		f.write(string)


def main():
	start_page = int(input('请输入要查询的起始页：'))
	end_page = int(input('请输入要查询的截止页：'))
	for page in range(start_page,end_page + 1):
		print('第%d页评论开始爬取...'%page)
		request = handle_request(page)
		json_text = urllib.request.urlopen(request).read().decode()
		parse_json_text(json_text)
		print('第%d页爬取结束。'%page)
		time.sleep(2)


if __name__ == '__main__':
	main()