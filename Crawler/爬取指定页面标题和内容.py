import urllib.request
import urllib.parse
import os
import re
def handle_request(url, page = None):
    if page != None:
        url = url + str(page) + '.html'
    #print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    req = urllib.request.Request(url = url,headers=headers)
    return req
def get_text(c_href):
    req = handle_request(c_href)
    response = urllib.request.urlopen(req).read().decode()
    pattern = re.compile(r'<div class="neirong">(.*?)</div>',re.S)
    la = pattern.findall(response)
    text = la[0]
    pat = re.compile(r'<p><img title=.*?></p>',re.S)
    text = pat.sub('',text)

    return text
    #print(la)

def chapter_content(content):
    pattern = re.compile(r'<h3><a href="(/lizhi/qianming/\d+\.html)"><b>(.*?)</b></a></h3>',re.S)
    lt = pattern.findall(content)
    #print(lt)
    #print(len(lt))
    for href in lt:
        c_href = 'http://www.yikexun.cn'+href[0]
        title = href[1]
        text = get_text(c_href)
        #print(text)
        string = '<meta http-equiv="Content-Type"content="text/html:charset=utf-8"><h1>%s</h1>%s'%(title,text)
        with open('lizhi.html','a',encoding='utf-8')as f:
            f.write(string)
def main():
    url = 'http://www.yikexun.cn/lizhi/qianming/list_50_'
    start_page = int(input('输入要查询的起始页：'))
    end_page = int(input('输入要查询的截至页：'))
    for page in range(start_page,end_page + 1):
        req = handle_request(url,page)
        content = urllib.request.urlopen(req).read().decode()
        chapter_content(content)


if __name__ == '__main__':
    main()