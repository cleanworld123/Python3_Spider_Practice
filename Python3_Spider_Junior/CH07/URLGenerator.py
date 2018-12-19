import re
import requests

'''
获取所有作者url信息，
结果以元组形式返回:
包含基本地址（str）、作者id和姓名（list）
'''
class URLGenerator(object):

    def geturltuple(self):
        #作者列表页面url
        basic_url = 'https://so.gushiwen.org/authors/'
        req_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }

        basic_html = self._get_html(basic_url, req_headers)
        # 获取作者信息列表，包含作者id和姓名
        pattern_author = re.compile(r'<a href="/authorv_(.*?).aspx">(.*?)</a>', re.DOTALL)
        authorinfolist = re.findall(pattern_author, basic_html)

        #获取分离出来的url信息元组，包含基本地址（str）、作者id和姓名（list）
        urltuple = self._generateurltuple(authorinfolist)
        return urltuple

    # 网页请求抓取
    def _get_html(self,url, localheaders):
        res = requests.get(url, headers = localheaders)
        if res.status_code == requests.codes.ok:
            html = res.text
            return html
        return ''

    # 组合url元组
    def _generateurltuple(self,infolist):
        # 定义每个作者首页URL的基础部分
        start_url = 'https://so.gushiwen.org/authors/authorvsw.aspx?'
        # 获取作者id和姓名列表
        idlist = infolist.group(1)
        namelist = infolist.group(2)
        return (start_url, idlist, namelist)


