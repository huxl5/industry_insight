#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/27 18:12 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/weixin_44566452/article/details/121039032

# 关闭警告
import warnings

warnings.filterwarnings("ignore")

from selenium import webdriver
from time import sleep
import pandas as pd
import datetime
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import functools


def log(text):
    print('-' * 15)
    print(text)


def logging(func):
    def wrapper(*args, **kw):
        try:
            print('%s %s():' % ('excute', func.__name__))
            return func(*args, **kw)
        except Exception as e:
            print('错误明细是', e.__class__.__name__, e)

    return wrapper


class find_document_jc(object):

    def __init__(self, stock_list):
        self.done_list = []
        self.stock_list = stock_list
        self.stock_list_neat = [stock[-6:] for stock in self.stock_list]
        self.current_dir = os.getcwd()
        date = str(datetime.date.today())
        self.work_dir = os.path.join(self.current_dir, date)

        @logging
        def set_driver(self):
            download_dir = self.work_dir
            options = Options()
            options.page_load_strategy = 'normal'
            options.add_experimental_option('prefs', {
                "download.default_directory": download_dir,  # 更改默认下载地址
                "download.prompt_for_download": False,  # 自动下载文件
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # 不直接在chrome内显示pdf
            })
            return options

        self.driver = webdriver.Chrome(options=set_driver(self))
        self.jc_web = 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index'

    @logging
    def set_work_dir(self):
        work_dir = self.work_dir
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)
            log('创建文件夹“%s”' % work_dir)
        else:
            log('文件夹“%s”已存在' % work_dir)

    @logging
    def file_rename(self, file_name, work_dir):
        flag = 0
        while flag == 0:
            try:
                file_list = os.listdir(work_dir)
                file_list.sort(key=lambda fn: os.path.getmtime(work_dir + "\\" + fn))
                target_file = file_list[-1]
                old = os.path.join(work_dir, target_file)
                new = os.path.join(work_dir, file_name)
                assert target_file[-3:].lower() == 'pdf'
                flag = 1
                if not os.path.exists(new):
                    log('找到目标文件，开始改名')
                    print('From:' + old)
                    print('To:' + new)
                    os.renames(old, new)
                else:
                    log('文件已存在：' + new)
            except Exception as e:
                print('错误明细是', e.__class__.__name__, e)
                print('错误,等待三秒后重试：可能由于【文件未下载完成】或【文件已存在】导致')
                sleep(3)

    def jc_file_name(self, r, results):
        code = results[r - 2].text
        stock = results[r - 1].text
        file = results[r].text
        file_name = '_'.join([code, stock, file])
        return file_name

    @logging
    def jc_search(self):
        # 获取内容
        results = self.driver.find_elements(By.CLASS_NAME, 'ahover')
        flag = 0
        # 遍历内容
        for r, result in enumerate(results):
            text = result.text
            if '初步询价' in text:
                file_name = self.jc_file_name(r, results)
                print(f'正在下载：{file_name}')
                href = result.find_element(By.XPATH, './a').get_attribute('href')
                print('进入下载页面：' + href)
                self.driver.get(href)
                download_icon = self.driver.find_element(By.CLASS_NAME, 'icongonggaoxiazai')
                download_icon.click()
                self.done_list.append(text)
                sleep(5)
                flag = 1
                self.flag_search = 1
                break
        if flag != 1:
            self.driver.find_element(By.CLASS_NAME, 'btn-next').click()

    @logging
    def jc(self, stock, stock_neat):
        self.flag_search = 0
        _driver = self.driver
        _driver.get(self.jc_web)
        _driver.implicitly_wait(10)
        sleep(3)
        search_line = _driver.find_elements(By.CLASS_NAME, 'el-input__inner')
        search_line[2].send_keys(stock_neat)
        sleep(3)
        search_icon = _driver.find_element(By.CLASS_NAME, 'el-button--primary')
        search_icon.click()
        log(f'目标股票：{stock_neat}')
        print('开始搜索文件：')
        # 搜索文件
        while self.flag_search != 1:
            self.jc_search()
        file_name = stock + '.pdf'
        # 重命名文件
        self.file_rename(file_name, self.work_dir)
        sleep(5)
        # 下载文件

    @logging
    def get_document(self):
        # 整理股票顺序
        stock_list_neat = self.stock_list_neat
        print(stock_list_neat)
        # 遍历股票
        for stock, stock_neat in zip(tqdm(stock_list), stock_list_neat):
            # 检查股票代码
            assert stock[-6:] == stock_neat
            self.jc(stock=stock, stock_neat=stock_neat)
        sleep(10)
        self.driver.quit()
        log('已获取文件：')
        list(map(lambda x: print(x), self.done_list))


if __name__ == '__main__':
    stock_list = '424-2021-10-11-688553,425-2021-10-11-688737,426-2021-10-11-301082,427-2021-10-11-688255,' \
                 '428-2021-10-12-301087,429-2021-10-13-688211,430-2021-10-14-301090,431-2021-10-14-301088,' \
                 '432-2021-10-14-688280,433-2021-10-14-688257,434-2021-10-18-301093,435-2021-10-18-688739,' \
                 '436-2021-10-18-301092'.split(',')

    func = find_document_jc(stock_list=stock_list)
    func.get_document()