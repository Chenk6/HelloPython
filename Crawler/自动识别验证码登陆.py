import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from PIL import ImageEnhance

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

def download_code(s):
    url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
    r = s.get(url=url,headers = headers)
    soup = BeautifulSoup(r.text,'lxml')
    image_src = soup.select('#imgCode')[0]['src']
    image_src = 'https://so.gushiwen.org' + image_src
    # print(image_src)
    res = s.get(url = image_src,headers = headers)
    with open('code.png','wb')as fp:
        fp.write(res.content)
    #查找表单数据
    __VIEWSTATE = soup.select('#__VIEWSTATE')[0]['value']
    __VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
    # # print(__VIEWSTATEGENERATOR)
    return __VIEWSTATE,__VIEWSTATEGENERATOR


def login(view, viewg, s):
    post_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
    #验证码识别
    img = Image.open('code.png')
    img = img.convert('RGB')
    enhancer = ImageEnhance.Color(img)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    img = enhancer.enhance(20)
    img = img.convert('L')#转化为灰度照片
    threshold = 140#二值化处理
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = img.point(table, '1')
    code = pytesseract.image_to_string(out)

    form_data = {
    '__VIEWSTATE':view,
    '__VIEWSTATEGENERATOR':	viewg,
    'from':'http://so.gushiwen.org/user/collect.aspx',
    'email':'1090509990@qq.com',
    'pwd':'123456',
    'code':	code,
    'denglu':'登录'
    }
    r = s.post(url = post_url,headers = headers,data=form_data)
    with open('poem.html','w',encoding='utf-8')as fp:
        fp.write(r.text)


def main():
    s = requests.Session()
    print('开始下载验证码')
    view,viewg = download_code(s)
    print('验证码下载完成')
    login(view,viewg,s)#携带得到的表单数据进行登录

if __name__ == '__main__':
    main()