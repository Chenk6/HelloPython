import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import time

class QianChengSpider(object):
    url1 = 'https://search.51job.com/list/010000,000000,0000,00,9,99,'
    url2 = '?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    def __init__(self, kw, start_page, end_page):
        self.kw = kw
        self.start_page = start_page
        self.end_page = end_page
        self.items = []

    def handle_request(self,page):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        kw = self.kw
        p = str(page) +'.html'
        url = self.url1 + kw + ',2,' + p +self.url2
        #print(url)
        req = urllib.request.Request(url = url,headers = headers)
        return req
    def prase_content(self,content):
        soup = BeautifulSoup(content, 'lxml')

        div_list = soup.select('#resultList > div')[3:-5]

        # print(div_list)
        # print(len(div_list))
        for div in div_list:
            t1 = div.select('.t1 > span > a')[0].string
            t1 = t1.strip()
            # print(t1)
            # exit()
            t2 = div.select('.t2 > a')[0].text
            t3 = div.select('.t3 ')[0].string
            t4 = div.select('.t4 ')[0].text
            t5 = div.select('.t5 ')[0].text

            item = {
                '职位名称': t1,
                '公司名称': t2,
                '公司地点': t3,
                '薪资': t4,
                '发布时间': t5
            }

            self.items.append(item)

    def run(self):
        for page in range(self.start_page,self.end_page + 1):
            print('第%s页开始爬取...'%page)
            req = self.handle_request(page)
            content = urllib.request.urlopen(req)
            self.prase_content(content)
            print('第%s页爬取结束。'%page)
            time.sleep(2)

        string = json.dumps(self.items, ensure_ascii=False)
        with open('qiancheng.txt', 'w', encoding='utf-8')as f:
            f.write(string)


def main():
    kw = input('请输入工作关键字 : ')
    start_page = int(input('请输入要查询的起始页： '))
    end_page = int(input('请输入要查询的结束页： '))
    spider = QianChengSpider(kw, start_page, end_page)
    spider.run()


if __name__ == '__main__':
    main()