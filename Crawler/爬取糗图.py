import urllib.parse
import urllib.request
import re
import os


def handle_request(url,page):
    url = url + str(page) + '/'
    #print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    req = urllib.request.Request(url = url,headers=headers)
    return req


def download_image(content):
    pattern = re.compile(r'<div class="thumb">.*?<img src="(.*?)".*?></div>',re.S)
    lt = pattern.findall(content)
    #print(len(lt))

    for image_str in lt:
        image_str = 'https:' + image_str
        #print(image_str)
        dirname = 'qiutu'
        path = r'E:\Users\day9'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        path = os.path.join(path,dirname)
            #print(path)
        filename = image_str.split('/')[-1]
        filepath = os.path.join(path,filename)
        #print(filepath)
        print('%s开始下载'%filename)

        urllib.request.urlretrieve(image_str,filepath)
        #response = urllib.request.urlopen(image_str)
        #with open(filepath,'wb')as f:
            #f.write(response.read())

        print('%s下载结束' % filename)


def main():
    url = 'https://www.qiushibaike.com/imgrank/page/'
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page,end_page + 1):
        print('第%d开始下载'%page)
        req = handle_request(url,page)
        content = urllib.request.urlopen(req).read().decode()
        #print(content)
        download_image(content)
        print('第%d页下载结束'%page)



if __name__ == '__main__':
    main()
