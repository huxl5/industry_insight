#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/4 13:54 
# @Author : huxiaoliang
# @description :selenium爬虫简单测试
# @see：https://www.cnblogs.com/qlqwjy/p/16519286.html
'''
​ selenium 是驱动浏览器，模拟人操作
1、环境安装：
    1、chrome浏览器，chrome驱动，两者大版本一致，wins32也可；注意驱动存放位置
    2、pip install selenium
    3、from selenium import webdriver
2、demo


'''

from selenium import webdriver

browser = webdriver.Chrome("chromedriver.exe")
browser.get("https://www.jd.com/")

# 获取网页源码
content = browser.page_source
print(content)
# 打印url
print(browser.current_url)

# 保存为图片(注意这里只能保存为png，不支持jpg)
browser.save_screenshot("jd.png")

# 打印title
print(browser.title)
# 窗口最大化
browser.maximize_window()

# 关闭
browser.close()
