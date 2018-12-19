from urllib import request
import re
import os

#请求贴吧目标页面
def getHtml(url):
    page = request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

#提取图片url，并进行下载
def getImg(html):
    #通过正则提取图片url
    reg = r'height="373" src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)

    #提取图片
    x = 0
    print('开始下载，共%d张图片。' % len(imglist))
    for imgurl in imglist:
        request.urlretrieve(imgurl,os.path.join('pictures', '%s.jpg' % x))
        x+=1
    print('下载完成!')

if __name__ == "__main__":
    url = 'https://tieba.baidu.com/p/5947539820'
    html = getHtml(url)
    getImg(html)

