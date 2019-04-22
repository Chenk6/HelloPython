import urllib.request
import urllib.parse
from lxml import etree
import time

item_list = []
def handle_request(url, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    url = url.format(page)
    #print(url)
    req = urllib.request.Request(url = url,headers=headers)
    return req


def parse_content(content):
    #生成对象
    tree = etree.HTML(content)
    div_list = tree.xpath('//div[@id="content-left"]/div')
    for odiv in (div_list):
        au = odiv.xpath('.//div[@class="author clearfix"]/a[last()]/h2/text()')
        author = au[0].replace('\n','')
        cont = odiv.xpath('.//a[@class="contentHerf"]/div/span')
        string = cont[0].xpath('string(.)')
        text = string.replace('\n','').replace('\t','')
        #print(author,text)
        #exit()
        item = {
            'author':author,
            'text':text
        }
        item_list.append(item)

def main():
    start_page = int(input('请输入起始页码 ：'))
    end_page = int(input('请输入结束页码 ：'))
    url = 'https://www.qiushibaike.com/hot/page/{}/'
    for page in range(start_page,end_page + 1):
        print('第%d页开始爬取:'% page)
        request = handle_request(url,page)
        content = urllib.request.urlopen(request).read().decode()
        parse_content(content)
        print('第%d页爬取结束:'% page)
        time.sleep(2)

    with open('qiushi.txt','w',encoding='utf-8')as f:
        f.write(str(item_list))
if __name__ == '__main__':
    main()