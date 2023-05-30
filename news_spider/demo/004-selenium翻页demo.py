#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/6 14:13 
# @Author : huxiaoliang
# @Description : 
# @See：
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# browser = webdriver.Firefox()
# browser = webdriver.Ie()
browser = webdriver.Chrome()
# 百度网页
browser.get("http://www.baidu.com")
browser.find_element(value="kw").send_keys(u"selenium")
# browser.find_element(by=By.XPATH,value='//*[@id="s_tab"]/div/a[1]').click()
time.sleep(2)
browser.find_element(value="su").click()
time.sleep(3)
# 百度资讯
# browser.get("http://www.baidu.com")
# input = browser.find_element(value="ww").send_keys("阿里巴巴")
# button = browser.find_element(value="s_btn_wr").click()
# 首頁問題
print('0:',browser.current_url)
browser.find_element(by = By.PARTIAL_LINK_TEXT,value='下一页').click()
print('1:',browser.current_url)
time.sleep(3)
browser.find_element(by = By.PARTIAL_LINK_TEXT,value='上一页').click()
print('2:',browser.current_url)
for i in range(4):
    time.sleep(3)
    # next = browser.find_element_by_link_text("下一页 ")
    next = browser.find_element(by = By.PARTIAL_LINK_TEXT,value='下一页')
    # pagelist = driver.find_element_by_class_name("pagelist")
    # next = browser.find_elements_by_class_name("n")
    # next = browser.find_element(by = By.CLASS_NAME,value= "n")
    next.click()
    # next.click()
    # nextBtn = browser.find_element(by=By.XPATH, value="//a[@class='n']")
    # nextBtn.click()
    # browser.find_element_by_partial_link_text("下一页").click()
    # body = browser.find_element_by_tag_name("body");
    # if "github" in body.text.encode("utf-8"):
    #     print("---Found it---")
    # else:
    #     print("---Not Found!---")
    print(browser.current_url)
    print("page:" + str(i))

time.sleep(6)
browser.quit()