import requests
from lxml import etree
items = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
url = 'https://beijing.8684.cn'
def parse_navigation():

    r = requests.get(url=url,headers = headers)
    #获取所有的导航链接
    tree = etree.HTML(r.text)
    number_list = tree.xpath('//div[@class = "bus_kt_r1"]/a/@href')
    char_list = tree.xpath('//div[@class = "bus_kt_r2"]/a/@href')
    # print(number_list + char_list)
    return number_list + char_list


def parsr_sanji_route(r):
    tree = etree.HTML(r.text)
    bus_site_name = tree.xpath('//div[@class = "bus_i_t1"]/h1/text()')[0]#公交线路名
    bus_site_name = bus_site_name.split('&')[0]
    run_time_info = tree.xpath('//div[@class = "bus_i_content"]/p/text()')[0]#线路运行时间
    ticket_info = tree.xpath('//div[@class = "bus_i_content"]/p/text()')[1]#票价信息
    company_info = tree.xpath('//div[@class = "bus_i_content"]/p')[2]#公交公司
    company_info = company_info.xpath('string(.)')
    updata_info = tree.xpath('//div[@class = "bus_i_content"]/p/text()')[3]#最后更新时间
    total_positive_site = tree.xpath('//span[@class = "bus_line_no"]/text()')[0]#正行线路总站数
    total_positive_site = total_positive_site.replace('\xa0', '')#去除空格
    bus_positive_site = tree.xpath('//div[@class = "bus_line_site "][1]/div/div/a/text()')  # 正行公交线路的所有站点信息
    try:
        total_reverse_site = tree.xpath('//span[@class = "bus_line_no"]/text()')[1]#反向公交线路的所有站点信息
        total_reverse_site = total_reverse_site.replace('\xa0', '')
        bus_reverse_site = tree.xpath('//div[@class = "bus_line_site "][2]/div/div/a/text()')  # 反行公交线路的所有站点信息
    except Exception as e:
        total_reverse_site = ''
        bus_reverse_site = []
    item = {
        '线路名': bus_site_name,
        '运行时间': run_time_info,
        '票价信息': ticket_info,
        '更新时间': updata_info,
        '正行站数': total_positive_site,
        '正行站点': bus_positive_site,
        '反行站数': total_reverse_site,
        '反行站点': bus_reverse_site,
    }
    items.append(item)
    # print(items)
    # exit()

def parse_erji_route(r):
    #查找每个线路
    tree = etree.HTML(r.text)
    route_name = tree.xpath('//div[@id = "con_site_1"]/a/@title')
    route_list = tree.xpath('//div[@id = "con_site_1"]/a/@href')
    i = 0
    for route in route_list:
        print('开始爬取%s'%route_name[i])
        url2 = url + route
        r = requests.get(url = url2,headers = headers)
        parsr_sanji_route(r)
        print('结束爬取%s'%route_name[i])
        i = i+1

def parse_erji_navigation(navi_list):
    #遍历获取以数字和字母开头的所有公交线路
    for erji_url in navi_list:
        url1 = url + erji_url
        print('开始爬取%s的所有线路信息'%url1)
        r = requests.get(url = url1,headers = headers)
        parse_erji_route(r)
        print('结束爬取%s的所有线路信息'%url1)


def main():
    #爬取第一页所有的导航链接
    navi_list = parse_navigation()
    parse_erji_navigation(navi_list)

    fp = open('gongjiao.txt','w',encoding='utf-8')
    for item in items:
        fp.write(str(item) + '\n')
    fp.close()

if __name__ == '__main__':
    main()