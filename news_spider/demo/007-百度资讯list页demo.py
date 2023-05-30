#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/6 9:22 
# @Author : huxiaoliang
# @Description : pipline:通过关键字爬取百度资讯的list页，TODO：记录url，进行解析
# @See：
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import threading
import time
from lxml import etree
from queue import Queue
import re
from bs4 import BeautifulSoup


class BaiduSpider(object):
    def __init__(self):
        # 百度首页
        # self.url = 'https://www.baidu.com/'
        # 百度资讯
        self.url = 'https://news.baidu.com/'
        # self.clear_page_num()
        self.page_num = self.read_page_num()
        self.driver = webdriver.Chrome()
        self.writer_2_csv = self.writer_2_csv()
        self.q = Queue()

    # 读取最后爬取过的页数
    def read_page_num(self):
        with open('已爬取URL.csv', 'r') as f:
            f = csv.reader(f)
            page_num = list(f)[-1][0]
            print(page_num)
        return page_num
    def clear_page_num(self):
        with open('已爬取URL.csv', 'r') as f:
            with open('已爬取URL.csv', 'a', newline='') as f:
                w = csv.writer(f)
                w.writerow([0])
        # 将已爬取的页数写入本地

    def save_page_num(self):
        url = self.driver.current_url
        page_num = re.search('&pn=(\d+)', url)
        if page_num is None:
            url += '&pn=0'
            page_num = re.search('&pn=(\d+)', url)
        with open('已爬取URL.csv', 'a', newline='') as f:
            w = csv.writer(f)
            w.writerow([page_num.group(1)])
        # cur_page_num = re.search('&pn=(\d+)', url)
        # if cur_page_num is None:
        #     cur_page_num = 0
        # with open('已爬取URL.csv', 'a', newline='') as f:
        #     w = csv.writer(f)
        #     w.writerow([cur_page_num])
    # 获取首页
    def get_first_page(self):
        self.driver.get(self.url)
        # self.driver.find_element('kw').send_keys('CEO辞职')
        # self.driver.find_element('su').click()
        self.driver.find_element(value="ww").send_keys('CEO辞职')
        self.driver.find_element(value="s_btn_wr").click()
        time.sleep(2)
        # self.parse_page()
        # self.click_next_page()

    # 解析页面,写入文件
    def parse_page(self):
        response = self.driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        hrefs = []
        for element in soup.find_all('div', class_='result-op c-container xpath-log new-pmd'):
            title = element.h3.a.attrs['aria-label'].strip()
            href = element.h3.a.attrs['href']
            hrefs.append(href)
            abstract = element.find('span', class_='c-font-normal c-color-text').attrs['aria-label'].strip()
            source = element.find('span', class_='c-color-gray').attrs['aria-label']
            publish_time = None
            if element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall'):
                publish_time = element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall').attrs[
                    'aria-label'].strip()

            # 获取正文

            dic = {
                '标题': title,
                '链接': href,
                '摘要': abstract,
                '发布时间': publish_time,
                '新闻来源': source
            }
            self.writer_2_csv.writerow(dic)  # 将数据输入到csv文件中



        # html = etree.HTML(response)
        # hrefs = html.xpath('//div[@class="result c-container "]/h3[@class="t"]/a/@href')
        # flag = html.xpath('//div[@id="page"]/a[last()]/@class')[0]
        # TODO 处理最后一页
        flag = 'n'
        if self.read_page_num()==50:
            flag = 'end'
            # 清空url文件 TODO
        return flag, hrefs

    # see：https://blog.csdn.net/qq_52200688/article/details/122324456
    def writer_2_csv(self):
        # 打开文件
        f = open('CEO辞职.csv', mode='a', encoding='utf-8', newline='')
        # 文件列名
        csv_writer = csv.DictWriter(f, fieldnames=['标题',
                                                   '链接',
                                                   '摘要',
                                                   '发布时间',
                                                   '新闻来源'],delimiter='`')
        # 输入文件列名
        csv_writer.writeheader()
        return csv_writer


    # 点击下一页, 感觉显示、隐式等待是个摆设，所以自己封装了个等待。
    # 其实可以使用retring模块，重发几次再报错休眠，人为处理
    def click_next_page(self):
        try:
            # self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()
            # self.driver.find_element(by=By.XPATH, value="//a[@class='n']").click()
            # self.driver.find_element(by=By.XPATH, value='//div[@id="page"]/a[last()]').click()
            self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value='下一页').click()
        except:
            time.sleep(10)
            # # self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()
            # self.driver.find_element(by=By.XPATH, value="//a[@class='n']").click()
            # self.driver.find_element(by=By.XPATH, value='//div[@id="page"]/a[last()]').click()
            self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value='下一页').click()

    # 获取每一页数据, 开爬.
    def get_page_html(self):
        self.get_first_page()
        while True:
            # 判断每一页URL是否已经爬取，已爬取则不解析直接跳转一页
            page_url = self.driver.current_url
            # FIXME:处理第0页
            page_num = re.search('&pn=(\d+)', page_url)
            if page_num is None:
                page_url +='&pn=0'
                page_num = re.search('&pn=(\d+)', page_url)
            print(page_num.group(1), self.page_num)
            # 判断当前页数是否大于已爬取的页数
            if page_num.group(1) > self.page_num:
            # # 判断当前页数是否大于已爬取的页数
            # if page_num > self.page_num:
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
        # t = threading.Thread(target=self.get_detail_html)
        # t.start()


if __name__ == '__main__':
    zhuce = BaiduSpider()
    zhuce.run()

    # driver.find_element('id', 'kw').clear()  # 清空输入框，防止下次输入的时候会连着上一次的，最后导致所有关键字都在输入框中了 driver.quit() #关闭浏览器
