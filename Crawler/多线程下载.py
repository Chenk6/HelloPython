import requests
from queue import  Queue
import threading
from lxml import etree
import json
import time

#存放爬取网页线程
crawl_list = []
#存放解析网页线程
parse_list = []

class CrawlThread(threading.Thread):
    def __init__(self,name,page_queue,data_queue):
        super(CrawlThread,self).__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.url = 'http://www.fanjian.net/jiantu-{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }

    def run(self):
        print('%s.....线程开始'%self.name)
        while 1:
            # 判断采集线程何时退出
            if self.page_queue.empty():
                break
            # 从队列中取出页码
            page = self.page_queue.get()
            # 拼接url，发送请求
            url = self.url.format(page)
            r = requests.get(url, headers=self.headers)
            # 将响应内容存放到data_queue中
            self.data_queue.put(r.text)
        print('%s.....线程结束'%self.name)
        # print(self.data_queue.qsize())

class ParseThread(threading.Thread):
    def __init__(self, name, data_queue, fp, lock):
        super(ParseThread, self).__init__()
        self.name = name
        self.data_queue = data_queue
        self.fp = fp
        self.lock = lock

    def run(self):
        print('%s.....线程开始'%self.name)
        while 1:
            data = self.data_queue.get(True, 10)
            # 解析内容即可
            self.parse_content(data)

        print('%s......线程结束'%self.name)

    def parse_content(self, data):
        tree = etree.HTML(data)
        # 先查找所有的li，再从li里面找自己的标题和url
        li_list = tree.xpath('//ul[@class="cont-list"]/li')
        # print(li_list)
        items = []
        for oli in li_list:
            # 获取图片标题
            title = oli.xpath('.//h2/a/text()')[0]
            # 获取图片url, 懒加载
            image_url = oli.xpath('.//div[contains(@class,"cont-list-main")]//img/@data-src')
            item = {
                '标题': title,
                '链接': image_url
            }
            items.append(item)
        # 写到文件中
        self.lock.acquire()
        self.fp.write(json.dumps(items, ensure_ascii=False) + '\n')
        self.lock.release()

def create_queue():
    #创建页码队列
    page_queue = Queue()
    for page in range(1,21):
        page_queue.put(page)
    #创建网页源码内容队列
    data_queue = Queue()
    return page_queue,data_queue

#创建爬取网页线程
def create_crawl_thread(page_queue, data_queue):
    crawl_name = ['crawl_thread1','crawl_thread2','crawl_thread3']
    for name in crawl_name:
        #创建一个爬取线程
        cthread = CrawlThread(name,page_queue,data_queue)
        crawl_list.append(cthread)

#创建解析网页线程
def create_parse_thread(data_queue,fp,lock):
    parse_name = ['parse_thread1','parse_thread2','parse_thread3']
    for name in parse_name:
        pthread = ParseThread(name,data_queue,fp,lock)
        parse_list.append(pthread)

def main():
    #创建队列函数
    page_queue,data_queue = create_queue()
    #打开文件
    fp = open('joke.json','a',encoding='utf-8')
    #创建锁
    lock = threading.Lock()
    #创建爬取网页线程
    create_crawl_thread(page_queue,data_queue)
    time.sleep(3)
    create_parse_thread(data_queue,fp,lock)

    #启动所有爬取网页线程
    for cthread in crawl_list:
        cthread.start()
    #启动所有解析网页线程
    for pthread in parse_list:
        pthread.start()

     #关闭所有爬取线程
    for cthread in crawl_list:
        cthread.join()
    #关闭所有解析线程
    for pthread in parse_list:
        pthread.join()

    fp.close()
    print('主子线程全部结束')

if __name__ == '__main__':
    main()