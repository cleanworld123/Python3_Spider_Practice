from Queuemanager import Queuemanager
from Downloader import Downloader
from DataParser import DataParser

class TaskScheduler:
    #建立类成员
    def __init__(self):
        #实例化其他几个功能模块
        self.queuemanager = Queuemanager()
        self.downloader = Downloader()
        self.parser = DataParser()

    #给下载器分配任务,逐个作者下载诗文,并按执行状态更新url列表
    def downloadallworks(self, base_url):
        i = 1   #下载作者计数
        while len(self.queuemanager.beforedownloadset) > 0:
            #1）从未下载队列中获取一个待下载作者，传到正在下载队列中
            newauthor = self.queuemanager.getnewauthor()

            # 2）下载当前作者的全部作品
            print('开始下载第{num}个作者诗文：\n'.format(num=i))
            result = self.downloader.downloadworks_oneauthor(base_url, newauthor)

            # 3）完成下载后，将作者信息传到已下载队列
            if result == 'finished':
                self.queuemanager.setdoneauthor(newauthor)
            else:
                print(result)
                break
            i += 1

if __name__ == '__main__':
    # 1.初始化对象,通过队列管理器Queuemanager对象初始化3个队列
    scheduler = TaskScheduler()

    # 2.按种子url获取作者列表页面，提取待下载url信息。包括基础url（base_url)和全部作者信息（id,姓名）的元组列表authorsinfotuplelist
    seedurl = 'https://so.gushiwen.org/authors/'
    basic_html = scheduler.downloader.get_html(seedurl)
    base_url, authorsinfotuplelist = scheduler.parser.geturls_allauthors(basic_html)

    # 3.得到全部作者信息元组(作者id和姓名)列表后，去重、追加到未下载队列中
    scheduler.queuemanager.insertbeforedownloadset(authorsinfotuplelist)

    # 4.分配任务,遍历每个作者的所有作品，下载保存
    scheduler.downloadallworks(base_url)
