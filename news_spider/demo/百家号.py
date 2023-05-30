#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/11 11:52 
# @Author : huxiaoliang
# @Description : 
# @See：
import requests
from bs4 import BeautifulSoup
import sys
import time
# from openpyxl import workbook
# from openpyxl import load_workbook

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver

browser = webdriver.Chrome("chromedriver.exe")

# # 以不打开浏览器的方式设置代理
# option = webdriver.ChromeOptions()
# # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# option.add_argument("--headless")
# # 谷歌文档提到需要加上这个属性来规避bug
# option.add_argument('--disable-gpu')
# # 添加代理
# # option.add_argument("--proxy-server=http://221.11.233.111:4315")  # 设置代理，请求头等，以列表的形式传入多个参数
#
# browser = webdriver.Chrome(executable_path="chromedriver.exe", options=option)
# # browser.get("http://www.ipdizhichaxun.com/")
# # 隐式等待5秒
# browser.implicitly_wait(3)


browser.get("https://baijiahao.baidu.com/s?id=1762318451006835630&wfr=spider&for=pc")

# 获取网页源码
content = browser.page_source
soup = BeautifulSoup(content,'html.parser')
all_comments = soup.find_all("div", {'class': '_3ygOc lg-fl'})
text = ''
for comment in all_comments:
    text += comment.get_text()  # 只提取文字
print(text)
print(soup)
import os

curr_dir = os.getcwd()
print(curr_dir)
# file = open(curr_dir + '\demo.txt', 'w+', encoding='utf-8')
# with open('{}.html'.format(1),'w',encoding='utf-8',) as f:
#     f.write(content)
# exit()
# 打印url
print(browser.current_url)
# browser.switch_to.window(browser.window_handles[-1])
browser.implicitly_wait(2)
browser.get("https://baijiahao.baidu.com/s?id=1624046826302829351&wfr=spider&for=pc")
# 获取网页源码
content = browser.page_source
soup = BeautifulSoup(content,'html.parser')
all_comments = soup.find_all("div", {'class': '_3ygOc lg-fl'})
text = ''
for comment in all_comments:
    text += comment.get_text()  # 只提取文字
print(text)
browser.close()

exit()

#获取百家号内容
headers1 =  {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Host': 'baijiahao.baidu.com'
    }
def get_content(url_list):
    try:
        for url in url_list:
            clist=[] #空列表存储文章内容
            r1 = requests.get(url,headers=headers1,timeout=10)
            soup1 = BeautifulSoup(r1.text, "lxml")
            s1 = soup1.select('.article-title > h2:nth-child(1)')
            s2 = soup1.select('.date')
            s3 = soup1.select('.author-name > a:nth-child(1)')
            s4 = soup1.find_all('span',class_='bjh-p')
            title = s1[0].get_text().strip()
            date = s2[0].get_text().strip()
            source = s3[0].get_text().strip()
            for t4 in s4:
                para =  t4.get_text().strip()  #获取文本后剔除两侧空格
                content = para.replace('\n','') #剔除段落前后的换行符
                clist.append(content)
            content = ''.join('%s' %c for c in clist)
        #     ws.append([title,date,source,content])
            print([title,date])
        # wb.save('XXX.xlsx')
    except Exception as e:
        print("Error: ",e)
    finally:
        # wb.save('XXX.xlsx')   #保存已爬取的数据到excel
        print(u'OK!\n\n')
url_list = ['https://baijiahao.baidu.com/s?id=1762318451006835630&wfr=spider&for=pc']
get_content(url_list)