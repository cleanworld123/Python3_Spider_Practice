import requests
from urllib import request
from lxml import etree
import re

#确定种子URL
base_url = 'http://bing.plmeizi.com/'
#请求基本页面
response = requests.get(base_url)
#初步解析
text = response.content.decode('utf-8')
html = etree.HTML(text)

#建立URL队列
imgs = html.xpath('//div[@class="list "]//img')
#基于URL队列：1.提取了每张图片的URL，2.提取了图片的中文说明，3.确定图片名称，4.对每个URL地址，进行图片的请求和本地保存。
for img in imgs:
    img_url = re.sub(r'-listpic','',img.get('src'))
    img_illustrate = re.findall(r'(.*?)\s\(.*?\)',img.get('alt'))[0]
    img_filename = img_illustrate + '.jpg'
    request.urlretrieve(img_url,'Bing_每日美图/' + img_filename)