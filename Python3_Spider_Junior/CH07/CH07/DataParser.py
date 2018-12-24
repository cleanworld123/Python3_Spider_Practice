import re

class DataParser:

    #1.基于种子页面（作者列表页）提取最终url的全部信息：基本url、作者信息（id、姓名）
    def geturls_allauthors(self, seed_html):
        # 通过观察，直接设置基本url
        base_url = 'https://so.gushiwen.org/authors/authorvsw.aspx?'

        # 获取作者信息元组列表，每个元组为(作者id和姓名)
        authorsinfotuplelist = self.getinfo_allauthors(seed_html)
        return base_url, authorsinfotuplelist

    #1.1 通过正则提取所有作者信息元组列表，包括作者id和姓名
    def getinfo_allauthors(self,basic_html):
        # 获取作者信息元组列表，每个元组为(作者id和姓名)
        pattern_author = re.compile(r'<a href="/authorv_(\S*?).aspx">(.*?)</a>', re.DOTALL)
        authorsinfotuplelist = re.findall(pattern_author, basic_html)
        return authorsinfotuplelist

    # 2.提取当前作者作品的总页数
    def getpagecount(self, single_html):
        parttern_pagenumber = re.compile(r'<span>(.*?)/\s(.*?)页</span>', re.DOTALL)
        pagenumber = re.search(parttern_pagenumber, single_html).group(2)
        return int(pagenumber)

    # 3.解析提取每首诗内容
    def getworks_singlepage(self, single_html):
        # 提取标题列表
        parttern_title = re.compile(r'<div class="cont">.*?<b>(.*?)</b>', re.DOTALL)
        titlelist = re.findall(parttern_title, single_html)
        # 提取正文列表
        parttern_content = re.compile(r'<div class="cont">.*?<div class="contson" id=".*?">(.*?)</div>', re.DOTALL)
        contentlist = re.findall(parttern_content, single_html)
        # 清洗正文多余字符
        contentlist = self.washdata(contentlist)
        return titlelist, contentlist

    # 3.1清洗多余字符
    def washdata(self,oldcontentlist):
        newcontentlist = []
        for content in oldcontentlist:
            # 去掉爬取下来的多余标签和换行等空白字符
            content = re.sub(r'\s+?', '', content)
            content = re.sub(r'<.*?br.*?>', '\n', content)
            content = re.sub(r'<.*?p.*?>', '', content)
            content = re.sub(r'<.*?strong.*?>', '', content)
            content = re.sub(r'<.*?span.*?>', '', content)
            content = re.sub(r'<.*?div.*?>', '', content)
            content = re.sub(r'&quot;', '"', content)
            newcontentlist.append(content)
        return newcontentlist
