from URLGenerator import URLGenerator
from Downloader import Downloader
from DataParser import DataParser
from DataStore import DataStore

class TaskScheduler:
    #建立类成员
    def __init__(self):
        #实例化其他几个功能模块
        self.urlgen = URLGenerator()
        self.downloader = Downloader()
        self.parser = DataParser()
        self.datastore = DataStore()

        #建立3个url队列：未下载、正在下载、完成下载
        self.beforedownloadset = set()
        self.beingdownloadset = set()
        self.afterdownloadset = set()
        #设定种子url
        self.seedurl = 'https://so.gushiwen.org/authors/'

    #1.调用URLGenerator获取url列表，建立三个队列（集合）
    def generateurlset(self,seedurl):
        #获取所有作者对应的作品首页url信息：基本url、作者信息元组(id、姓名)的列表
        newbase_url, newauthorstuplelist = self.urlgen.geturltuple(seedurl)

        #作者信息元组去重后，添加到未下载队列beforedownloadset（集合）中
        self._addnewids(newauthorstuplelist)
        return newbase_url

    #2.给下载器分配任务,逐个作者下载诗文,并按执行状态更新url列表
    def downloadallworks(self, base_url):
        while len(self.beforedownloadset) > 0:
            #提取一个作者，放入正在下载队列
            authorinfo = self.beforedownloadset.pop()
            self.beingdownloadset.add(authorinfo)

            #开始下载当前作者的全部作品
            result = self.downloader.downloadforoneauthor(base_url,authorinfo)
            if result =='finished':
                # 完成下载，将作者信息放入已下载队列
                self.afterdownloadset.add(authorinfo)
                self.beingdownloadset.remove(authorinfo)
            else:
                print(result)
                break

    #得到新的id列表后，先去重，然后追加到未下载url队列后面
    def _addnewids(self, authorstuple):
        #通过集合的差集运算去除重复元素
        idset = set(authorstuple)
        idset = idset - self.beforedownloadset - self.beingdownloadset - self.afterdownloadset
        #去重后，通过集合的并集运算添加到未下载队列beforedownloadset中
        self.beforedownloadset = self.beforedownloadset | idset

if __name__ == '__main__':
    # 初始化对象
    scheduler = TaskScheduler()
    # 按种子url下载作者信息的元组列表
    base_url = scheduler.generateurlset(scheduler.seedurl)
    # 遍历每个作者的所有作品，下载保存
    scheduler.downloadallworks(base_url)
