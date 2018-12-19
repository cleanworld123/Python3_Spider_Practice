import requests
from bs4 import BeautifulSoup

#待抓取URL
url = 'https://www.qiushibaike.com/text/'

#1.请求抓取
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

#2.解析提取
soup = BeautifulSoup(html)
joke_content = soup.select('div.content')[0].get_text()

#3.展示结果
print(joke_content)