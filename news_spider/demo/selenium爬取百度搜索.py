#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/4 15:44 
# @Author : huxiaoliang
# @description :
from selenium import webdriver
import csv
import threading
import time
from lxml import etree
from queue import Queue
import re


class BaiduSpider(object):
    def __init__(self):
        self.url = 'https://www.baidu.com/'
        self.page_num = self.read_page_num()
        self.driver = webdriver.Chrome()
        self.q = Queue()

    # 读取最后爬取过的页数
    def read_page_num(self):
        with open('已爬取URL.csv', 'r') as f:
            f = csv.reader(f)
            page_num = list(f)[-1][0]
            print(page_num)
        return page_num

    # 获取首页
    def get_first_page(self):
        self.driver.get(self.url)
        # self.driver.find_element_by_name('wd').send_keys('注册页面')
        self.driver.find_element('wd').send_keys('注册页面')
        # self.driver.find_element_by_id('su').click()
        self.driver.find_element('su').click()
        time.sleep(3)
        self.click_next_page()

    # 解析页面
    def parse_page(self):
        response = self.driver.page_source
        html = etree.HTML(response)
        hrefs = html.xpath('//div[@class="result c-container "]/h3[@class="t"]/a/@href')
        flag = html.xpath('//div[@id="page"]/a[last()]/@class')[0]
        return flag, hrefs

    # 将已爬取的页数写入本地
    def save_page_num(self):
        url = self.driver.current_url
        page_num = re.search('&pn=(\d+)', url)
        with open('已爬取URL.csv', 'a', newline='') as f:
            w = csv.writer(f)
            w.writerow([page_num.group(1)])

    # 点击下一页, 感觉显示、隐式等待是个摆设，所以自己封装了个等待。
    # 其实可以使用retring模块，重发几次再报错休眠，人为处理
    def click_next_page(self):
        try:
            self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()
        except:
            time.sleep(10)
            self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()

    # 获取每一页数据, 开趴.
    def get_page_html(self):
        self.get_first_page()
        while True:
            # 判断每一页URL是否已经爬取，已爬取则不解析直接跳转一页
            page_url = self.driver.current_url
            page_num = re.search('&pn=(\d+)', page_url)
            print(page_num.group(1), self.page_num)
            # 判断当前页数是否大于已爬取的页数
            if page_num.group(1) > self.page_num:
                # 解析页面数据，判定是否到达末页，以及获取详情页的URL
                flag, urls = self.parse_page()
                # 判断是否为末页
                if flag != 'n':
                    print('已爬取百度全部数据')
                    break
                # 将详情页URL加入队列
                for url in urls:
                    self.q.put(url)
                # 将当前页面URL的页数保存至本地
                self.save_page_num()
                # 跳转至下一页 不想写显示等待，网不太好感觉还是会报错
                time.sleep(3)
                self.click_next_page()
            else:
                # 如果当前页数不大于已爬取页数，则点击下一页
                self.click_next_page()

    # 获取详情页
    def get_detail_html(self):
        while True:
            if self.q.qsize() != 0:
                url = self.q.get()
                print(url)
            else:
                time.sleep(5)

    def run(self):
        # 获取每页URL
        c = threading.Thread(target=self.get_page_html)
        c.start()
        # 解析详情页
        t = threading.Thread(target=self.get_detail_html)
        t.start()


if __name__ == '__main__':
    zhuce = BaiduSpider()
    zhuce.run()
