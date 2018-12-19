import re
import requests
import io
import time
import random

def crawl(start_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    page = 1
    id = '85097dd0c645'
    author = '白居易'
    filename = author+'.txt'
    # 建立URL队列，循环爬行全部308页白居易诗文
    personalworks_hommeurl = start_url + 'page=%s&id=%s' % (str(page),id)
    # 请求爬取个人作品首页，提取总页数，需要在消息头中带上浏览器信息
    works_html = get_html(personalworks_hommeurl, req_headers)
    pagecount = getpagenumber(works_html)
    print(pagecount)

    # 遍历所有个人作品页，获取每页的诗作
    for i in range(1, pagecount+1):
        eachpage_url = start_url + 'page=%s&id=%s' % (str(i),id)
        time.sleep(random.randint(3,6))
        singlepageworks_html = get_html(eachpage_url, req_headers)
        if len(works_html) > 0:
            # 获取每一首诗的内容,并以作者为文件名保存到本地
            with io.open(filename, mode='a', encoding='utf-8') as f:
                # 解析提取当前页中所有诗
                titlelist, contentlist = getsingledata(singlepageworks_html)

                # 写入文档
                f.write(u'第{pagenum}页：\n\n'.format(pagenum=i))
                print(u'第{pagenum}页：\n'.format(pagenum=i))

                for j in range(0, len(titlelist)-1):
                    print(u'正在获取 {title}'.format(title=titlelist[j]))
                    f.write(u'{title}{content}\n'.format(title=titlelist[j], content=washdata(contentlist[j])))

def getpagenumber(single_html):
    # 提取当前作者作品的总页数
    parttern_pagenumber = re.compile(r'<span>(.*?)/\s(.*?)页</span>', re.DOTALL)
    pagenumber = re.search(parttern_pagenumber, single_html).group(2)
    return int(pagenumber)

# 网页请求抓取
def get_html(url, localheaders):
    res = requests.get(url, headers = localheaders)
    if res.status_code == requests.codes.ok:
        html = res.text
        return html
    return ''

# 数据解析提取，得到每首诗内容
def getsingledata(single_html):
    # 标题
    parttern_title = re.compile(r'<div class="cont">.*?<b>(.*?)</b>', re.DOTALL)
    titlelist = re.findall(parttern_title, single_html)

    # 正文
    parttern_content = re.compile(r'<div class="cont">.*?<div class="contson" id=".*?">(.*?)</div>', re.DOTALL)
    contentlist = re.findall(parttern_content, single_html)
    return titlelist, contentlist

#清洗多余字符
def washdata(content):
    # 去掉爬取下来的多余标签
    content = re.sub(r'<br\s*/>', '\n', content)
    content = re.sub(r'<br>', '', content)
    content = re.sub(r'<p>', '', content)
    content = re.sub(r'</p>', '', content)
    content = re.sub(r'<span .*?>', '', content)
    content = re.sub(r'</span>', '', content)

    return content

if __name__ == '__main__':
    # 定义种子URL的基础
    start_url = 'https://so.gushiwen.org/authors/authorvsw.aspx?'
    # 开始爬
    crawl(start_url)