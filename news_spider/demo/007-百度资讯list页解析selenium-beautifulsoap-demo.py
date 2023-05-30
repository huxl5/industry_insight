#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/6 17:12 
# @Author : huxiaoliang
# @Description : 
# @See：

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

browser = webdriver.Chrome("chromedriver.exe")
browser.get("https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=CEO%E8%BE%9E%E8%81%8C&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8")

# 获取网页源码
content = browser.page_source
# print(content)
# 打印url
print(browser.current_url)

soup = BeautifulSoup(content, 'html.parser')
for element in soup.find_all('div', class_='result-op c-container xpath-log new-pmd'):
    # print(element)
    # print(element.h3)
    # print(element.a)
    print(element.h3.a.attrs['href'])
    print(element.h3.a.attrs['aria-label'])
    print(element.find('span', class_='c-font-normal c-color-text').attrs['aria-label'])
    pubulish_time = None
    if element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall'):
        pubulish_time = element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall').attrs['aria-label']
    print(pubulish_time)
    print(element.find('span',class_='c-color-gray').attrs['aria-label'])
