from DataParser import DataParser
from DataStore import DataStore
import requests
import time
import random
from fake_useragent import UserAgent

class Downloader(object):
    #建立类成员
    def __init__(self):
        #实例化同级类
        self.parser = DataParser()
        self.datastore = DataStore()

    # 1.通用的网页请求抓取
    def get_html(self, url):
        try:
            # 使用随机User-Agent
            ua = UserAgent()
            req_headers = {'User-Agent': ua.random}

            res = requests.get(url, headers=req_headers)
            if res.status_code == requests.codes.ok:
                html = res.text
                return html
            return ''
        except Exception as e:
            return e

    # 2.下载指定作者的所有作品
    def downloadworks_oneauthor(self, start_url, authorinfotuple):
        # 1）提取作者信息，并设置请求的完整url和结果记录文件名
        pagenum = 1
        authorid = authorinfotuple[0]
        authorname = authorinfotuple[1]

        # 2）组成目标页面URL，循环爬行当前作者全部诗文
        personalworks_hommeurl = start_url + 'page=%s&id=%s' % (str(pagenum), authorid)

        # 3)遍历所有页面，下载并保存到文件中
        try:
            # i.爬取个人作品首页，提取总页数
            works_html = self.get_html(personalworks_hommeurl)
            pagecount = self.parser.getpagecount(works_html)

            # ii.创建文档，写入基本信息
            totalinfo = u'\n作者:{name},页数：{pagecount}\r\n'.format(name=authorname, pagecount=pagecount)
            path = u'作品集'
            filename = path + '\\' + authorname + '.txt'
            self.datastore.createfile_oneauther(filename, path, totalinfo)

            # iii.遍历作者所有作品页，提取诗文保存到指定文档
            for i in range(1, pagecount + 1):
                #组合每一页的url
                page_url = start_url + 'page=%s&id=%s' % (str(i), authorid)
                #请求抓取当前诗文页面
                time.sleep(random.randint(3, 6))
                singlepageworks_html = self.get_html(page_url)
                if len(works_html) > 0:
                    # 提取当前页中所有诗文
                    titlelist, contentlist = self.parser.getworks_singlepage(singlepageworks_html)
                    # 写入文档
                    self.datastore.storeworks_singlepage(filename, i, titlelist, contentlist)
            return 'finished'
        except Exception as e:
            return e



