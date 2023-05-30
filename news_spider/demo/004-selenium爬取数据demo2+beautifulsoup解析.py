#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/4 14:24 
# @Author : huxiaoliang
# @description :
'''
一个简单的例子，过程如下：
1.打开百度首页，睡眠2s
2.输入java，睡眠2s
3.点击百度一下按钮，睡眠5s
4.滚动到底部，睡眠5s
5.翻到第二页，睡眠5s
6.点击后退回退到第一页，睡眠5s
7.点击前进再回去第二页， 睡眠5s
8.结束
'''
import time

from selenium import webdriver

from selenium.webdriver.common.by import By

import re
from bs4 import BeautifulSoup

from lxml import etree

browser = webdriver.Chrome("chromedriver.exe")
# 1.打开百度首页，睡眠2s
# browser.get("https://www.baidu.com/")
browser.get("https://news.baidu.com/")
time.sleep(1)

# 2.输入java，睡眠2s
# input = browser.find_element(value="kw")
input = browser.find_element(value="ww")
input.send_keys("阿里巴巴")
time.sleep(1)

# 3.点击百度一下按钮，睡眠5s
button = browser.find_element(value="s_btn_wr")
button.click()
time.sleep(1)



# 4.滚动到底部，睡眠5s
js = 'document.body.scrollTop=100000'
browser.execute_script(js)

# 解析页面
# print(browser.text)
# print(browser.page_source)
res = browser.page_source
# 直接解析

# # BeautifulSoup
# res.encoding = 'utf8'
# print(res.text)
soup = BeautifulSoup(res,'html.parser')
# print(soup.prettify())
# print(soup.h3)
for element in soup.find_all(['h3']):
    # print(element)
    a = element.find('a')
    print(a)
    print(a.attrs['aria-label'])
    print(a.attrs['href'])
    # if a.string!=None:
    #     print(a.string)
    #     print(a.get("href"))

# etree
# html = etree.HTML(response)
# hrefs = html.xpath('//div[@class="result c-container "]/h3[@class="t"]/a/@href')
# flag = html.xpath('//div[@id="page"]/a[last()]/@class')[0]
time.sleep(2)
exit()



# 5.翻到第二页，睡眠5s
nextBtn = browser.find_element(by=By.XPATH, value="//a[@class='n']")
nextBtn.click()

# 4.滚动到底部，睡眠5s
js = 'document.body.scrollTop=100000'
browser.execute_script(js)

# 解析页面
# print(browser.text)
# print(browser.page_source)
res = browser.page_source
# 直接解析
# 2.  获取信息的网址和标题
# 获取信息的网址
p_href = '<h3 class="news-title_1YtI1 "><a href="(.*?)"'
href = re.findall(p_href, res)
print(href)

# 获取信息的标题
p_title = '<h3 class="news-title_1YtI1 ">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)
print(title)

# 3. 获取信息的来源和日期
# 获取信息的来源
p_source = '<span class="c-color-gray" aria-label=.*?>(.*?)</span>'
source = re.findall(p_source, res)
print(source)

# 获取信息的日期
p_date = '<span class="c-color-gray2 c-font-normal c-gap-right-xsmall" aria-label=".*?>(.*?)</span>'
date = re.findall(p_date, res)
print(date)

# 获取信息的摘要和正文



# 4.  数据清洗和打印输出
# 数据清洗和打印输出 # FIXME：10条取到7条，后三条不知为啥了：原因：有的时间没有
for i in range(len(title)):  # range(len(title)),这里因为知道len(title) = 10，所以也可以写成for i in range(10)
    title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过这里好像不太需要了
    title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
    # print(str(i + 1) + '.' + title[i], source[i],date[i],href[i])  # print(1, 'hello') 这种写法，就是在同一行连续打印多个内容
    print(str(i + 1) + '.' + title[i], source[i],href[i])  # print(1, 'hello') 这种写法，就是在同一行连续打印多个内容
    # print(str(i + 1) + '.' + title[i] + ' ' + source[i] + ' ' + date[i])  # 这个是纯字符串拼接
    # print(href[i])   # 输出链接


time.sleep(2)

# 5.翻到第三页，睡眠5s
nextBtn = browser.find_element(by=By.XPATH, value="//a[@class='n']")
nextBtn.click()
time.sleep(2)

# 6. 点击后退回退到第二页，睡眠5s
browser.back()
time.sleep(2)

# 7. 点击前进再回去第三页， 睡眠5s
browser.forward()
time.sleep(2)

# 8. 关闭
browser.close()
