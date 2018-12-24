from DataParser import DataParser

class Queuemanager(object):
    # 建立类成员
    def __init__(self):
        #实例化同级类
        self.parser = DataParser()

        # 建立3个url队列：未下载、正在下载、完成下载
        self.beforedownloadset = set()
        self.beingdownloadset = set()
        self.afterdownloadset = set()

    #1.得到新的(作者id和姓名)元组列表后，先去重，然后追加到未下载set中
    def insertbeforedownloadset(self, authorstuplelist):
        #去重，通过集合的差集运算去除重复元素
        idset = set(authorstuplelist)
        idset = idset - self.beforedownloadset - self.beingdownloadset - self.afterdownloadset
        #去重后，通过集合的并集运算添加到未下载队列beforedownloadset中
        self.beforedownloadset = self.beforedownloadset | idset

    #2.弹出一个新的下载元组，从未下载set转到正在下载set
    def getnewauthor(self):
        if len(self.beforedownloadset) > 0:
            #提取一个作者，放入正在下载队列
            authorinfo = self.beforedownloadset.pop()
            self.beingdownloadset.add(authorinfo)
            return authorinfo

    # 3.设置刚完成下载的作者元组，从正在下载set转到已下载set
    def setdoneauthor(self, doneauthor):
        # 完成下载，将作者信息放入已下载队列
        self.afterdownloadset.add(doneauthor)
        self.beingdownloadset.remove(doneauthor)