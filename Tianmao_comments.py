from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from bs4 import BeautifulSoup
import time

def deal_recommends_infos(url):
   if not url.startswith('http'):
       url = 'https:' + url
   print('开始寻找评论:' + url)
   driver = webdriver.Chrome()
   driver.maximize_window() # 全屏

   timeout = 30
   try:
       driver.get(url)

       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.ID, "sufei-dialog-close"))  # 判断页面是否初步加载成功的标记
       )
       #!!!close the dialogbox onfront
       if EC.presence_of_element_located((By.ID, "sufei-dialog-close")):
           time.sleep(1)
           driver.find_element_by_id('sufei-dialog-close').click()

       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.ID, "J_TabBarBox"))  # 判断页面是否初步加载成功的标记
       )

   except TimeoutException:
       print('宝贝链接未加载成功')
   try:
       # 页面上拉600，看到TabBarBox
       js = "window.scrollTo(0,600)"
       driver.execute_script(js)
   except WebDriverException:
       print('上拉寻找评论区时出现问题')
   time.sleep(2)
   WebDriverWait(driver, timeout).until(
       EC.element_to_be_clickable((By.XPATH, '//*[@id="J_TabBar"]/li[2]'))  # 判断页面是否初步加载成功的标记
   )

   # 点击累计评论TAB
   driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]').click()

   time.sleep(4)
   print('成功点击累计评论TAB')
   try:
       # rate-grid的正则表达式
       driver.find_element_by_xpath('//*[@id="J_Reviews"]/div/div[6]')
   except NoSuchElementException:
       print('评论信息中元素还未加载')
   print('已经成功加载到评论区信息')

   #  for i in range(2):      # only 2 pages
   i = 1
   while True:   # try to download all pages, but anti-crawler exists, couldn't get all pages

        # close the dialogbox. anti-crawler exists, a dialog box is shown when downloads 16 pages or more
       if EC.presence_of_element_located((By.LINK_TEXT, "javascript:void(\'close\')")):
            time.sleep(3)
            if driver.find_element_by_xpath('//a[@href="javascript:void(\'close\')"]').is_enabled():
                driver.find_element_by_xpath('//a[@href="javascript:void(\'close\')"]').click()       

       try:
           # 页面上拉2500，看到评论区
           js = "window.scrollTo(0,2500)"
           driver.execute_script(js)
           time.sleep(2)
           # 点击下一页
           driver.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:last-child').click()

       except WebDriverException:
           js = "window.scrollTo(0,3500)"
           driver.execute_script(js)
           time.sleep(2)
           # 点击下一页
           try:
               driver.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:last-child').click()
           except NoSuchElementException:
               print('找不到评论')
               break
       except NoSuchElementException:
           print('找不到翻页按钮')
           continue
       print('已成功点击下一页')

       soup = BeautifulSoup(driver.page_source, "lxml")
       #提取评论信息
       comementdict = get_recommends_infos(soup)
       print(comementdict)

        # write into txt

       with open('comments.txt','a',encoding='utf-8') as f:
           f.write('page ' + str(i) + '\n' + str(comementdict) + '\n')
           i += 1

       hasnextpage = driver.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:last-child').is_enabled()
       if not hasnextpage:
          break
   print('完成该链接的评论抓取')


#提取评论信息
def get_recommends_infos(s):
    comment = s.find("div",class_="rate-grid")
    comment_data = comment.find_all("tr")
    lst1=[]
    #逐行读取
    for i in comment_data:
        goodstype_lst=[]
        username_lst=[]
        #comment1为初次评论，comment2为追加评论，reply1为商家初次回复，reply2为商家追加回复，goodstype为商品类型，username为用户名
        dic={'comment1': '','reply1':'','comment2': '','reply2':'', 'goodstype': goodstype_lst, 'username': username_lst}
        try:
            content1=i.find('div',class_="tm-rate-premiere").find('div',class_="tm-rate-content")
            dic['comment1']=content1.text
        except:
            content1=i.find('div',class_="tm-rate-content").find('div',class_="tm-rate-fulltxt")
            dic['comment1']=content1.text
        try:
            content2=i.find('div',class_="tm-rate-append").find('div',class_="tm-rate-content")
            dic['comment2']=content2.text
        except:
            dic['comment2']='null'

        try:
            reply1=i.find('div',class_="tm-rate-premiere").find('div',class_="tm-rate-reply")
            dic['reply1']=reply1.text
        except:
            try:
                reply2=i.find('div',class_="tm-rate-append").find('div',class_="tm-rate-reply")
                dic['reply1']='null'
            except:
                try:
                    reply1=i.find('div',class_="tm-rate-reply")
                    dic['reply1']=reply1.text
                except:
                    dic['reply1']='null'
        try:
            reply2=i.find('div',class_="tm-rate-append").find('div',class_="tm-rate-reply")
            dic['reply2']=reply2.text
        except:
            dic['reply2']='null'
        goodstype=i.find('div',class_="rate-sku").find_all('p')
        for b in goodstype:
            goodstype_lst.append(b.attrs['title'])
        username=i.find_all('div',class_="rate-user-info")
        for c in username:
            username_lst.append(c.text)
        lst1.append(dic)
    return lst1

if __name__ == '__main__':
    url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.26.67557e175B0Grk&id=555843337517&skuId=4611686574270725421&user_id=2406931838&cat_id=2&is_b=1&rn=b0555055e01a2fc7fa9eb08cfab43b75'
    deal_recommends_infos(url)