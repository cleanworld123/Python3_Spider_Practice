import re
import requests

'''
获取所有作者url信息，
结果以元组形式返回:
包含基本地址（str）、作者id和姓名（list）
'''
class URLGenerator(object):
    # 基于作者列表页面种子url提取作者url关键信息
    def geturltuple(self,seed_url):

        req_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        #定义作者作品集首页的基本url
        base_url = 'https://so.gushiwen.org/authors/authorvsw.aspx?'

        basic_html = self._get_html(seed_url, req_headers)
        # 获取作者信息元组列表，每个元组为(作者id和姓名)
        pattern_author = re.compile(r'<a href="/authorv_(\S*?).aspx">(.*?)</a>', re.DOTALL)
        authorsinfotuplelist = re.findall(pattern_author, basic_html)
        return base_url, authorsinfotuplelist

    # 网页请求抓取
    def _get_html(self,url, localheaders):
        res = requests.get(url, headers = localheaders)
        if res.status_code == requests.codes.ok:
            html = res.text
            return html
        return ''
'''
if __name__=="__main__":
    seedurl = 'https://so.gushiwen.org/authors/'
    urlgen = URLGenerator()
    urlgen.geturltuple(seedurl)
'''

