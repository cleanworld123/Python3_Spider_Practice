# -*- coding:utf-8 -*-
'''
白居易诗集，爬取第一页
'''

import re
import requests
import io

def crawl(start_url):
    base_url = 'http://so.gushiwen.org'
    #消息头中带上浏览器信息
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    print(start_url)

    # 请求爬取当前页所有内容，需要在消息头中带上浏览器信息
    starthtml = get_html(start_url, req_headers)
    if len(starthtml) > 0:
        # 解析提取当前页中所有诗的各自主页链接，建立了一个URL队列
        parttern_href = re.compile(r'<div class="cont">.*?<p><a .*? href="(.*?)" .*?>.*?</p>', flags=re.DOTALL)
        hrefs = re.findall(parttern_href, starthtml)

        # 解析提取每一首诗的内容,并保存到本地
        with io.open(u'白居易诗集.txt', mode='a', encoding='utf-8') as f:

            # 循环请求爬行URL队列对应的每首诗页面, 从中提取对应诗的内容
            for href in hrefs:
                href = base_url + href
                # 请求每首诗的页面
                innerhtml = get_html(href, req_headers)
                if len(innerhtml) > 0:
                    # 解析提取每首诗内容
                    singletitle, singlecontent = getsingledata(innerhtml)
                    print(u'正在获取 {title}'.format(title = singletitle))
                    #写入文档
                    f.write(u'{title}{content}\n'.format(title = singletitle, content = singlecontent))

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
    parttern_title = re.compile(r'<div class="cont">.*?<h1 .*?>(.*?)</h1>', re.DOTALL)
    title = re.search(parttern_title, single_html).group(1)
    # 正文
    parttern_content = re.compile(r'<div class="cont">.*?<div class="contson" id=".*?">(.*?)</div>',
                                  re.DOTALL)
    content = re.search(parttern_content, single_html).group(1)

    # 去掉爬取下来的多余标签
    content = re.sub(r'<br />', '\n', content)
    content = re.sub(r'<p>', '', content)
    content = re.sub(r'</p>', '', content)
    content = re.sub(r'<span .*?>', '', content)
    return title, content

if __name__ == '__main__':
    #定义了白居易的诗文全集首页为种子URL
    start_url = 'https://so.gushiwen.org/authors/authorvsw_85097dd0c645A1.aspx'
    #开始爬
    crawl(start_url)