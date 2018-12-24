from DataParser import DataParser
import os
import io

class DataStore:
    #建立类成员
    def __init__(self):
        #实例化同级类
        self.parser = DataParser()

    #1.创建当前作者文档，写入汇总信息
    def createfile_oneauther(self, filename, path, totalinfo):
        #创建路径
        self.mkpath(path)
        with io.open(filename, mode='w', encoding='utf-8') as f:
            f.write(totalinfo)

    #1.1创建诗文存放路径
    def mkpath(self,path):
        '''
        :param path: 存放文件夹
        '''
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建目录
            os.mkdir(path)

    #2.写入当前页所有诗文
    def storeworks_singlepage(self, filename, pagenum, titlelist, contentlist):
        #以追加方式写入
        with io.open(filename, mode='a', encoding='utf-8') as f:
            # 写入文档
            f.write(u'第{pagenum}页：\n\n'.format(pagenum = pagenum))
            print(u'第{pagenum}页：\n'.format(pagenum = pagenum))

            for j in range(0, len(titlelist) - 1):
                print(u'正在获取 {title}'.format(title=titlelist[j]))
                f.write(u'{title}\n{content}\n\n'.format(title=titlelist[j], content=contentlist[j]))

