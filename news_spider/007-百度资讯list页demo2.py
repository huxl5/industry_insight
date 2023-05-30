#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/6 9:22 
# @Author : huxiaoliang
# @Description : pipline:通过关键字爬取百度资讯的list页，
# @See：

# 关闭警告
import warnings

warnings.filterwarnings("ignore")

import csv
import re
import threading
import time
from queue import Queue

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import platform

curr_dir = os.getcwd()
print(curr_dir)
if platform.system().lower() == 'windows':
    project_path = r'D:\work_softs\workspace-py-citic\industry_insight\news_spider'
    driver_path = '/usr/bin/chromedrive'
elif platform.system().lower() == 'linux':
    project_path = '/root/projects'


def get_chrome_browser():
    option = webdriver.ChromeOptions()
    # 无头模式
    option.add_argument('headless')
    # 沙盒模式运行
    option.add_argument('no-sandbox')
    # 大量渲染时候写入/tmp而非/dev/shm
    option.add_argument('disable-dev-shm-usage')
    # 可选择指定驱动路径
    browser = webdriver.Chrome('D:\work_softs\workspace-py-citic\industry_insight\chromedriver.exe',options=option)
    # browser = webdriver.Chrome(options=option)
    return browser


# see：https://blog.csdn.net/qq_52200688/article/details/122324456
def writer2csv(keyword):
    # 打开文件
    if '"' in keyword:
        keyword = keyword.replace('"','')
        keyword = keyword+'-全匹配'
    f = open(os.path.join(project_path, 'baijiahao/{keyword}.csv'.format(keyword=keyword)), mode='w', encoding='utf-8',
             newline='')
    # 文件列名
    csv_writer = csv.DictWriter(f, fieldnames=['标题',
                                               '新闻来源',
                                               '发布时间',
                                               '摘要',
                                               '第n页',
                                               '第n条',
                                               '链接',
                                               '正文'], delimiter='`')
    # 输入文件列名
    csv_writer.writeheader()
    return csv_writer


def download_page(url, para=None):
    # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    #            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #            'referer': '',
    #            'Cookie':'BIDUPSID=EC6666002B7BB97BD387A45F8A26DCE0; PSTM=1588261875; BDUSS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; BDUSS_BFESS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; MCITY=-131%3A; __yjs_duid=1_8f7399597e04daa153a297b7b9dc5e701626970583238; BAIDUID=0409633BC907815247521A8C2EB736E6:FG=1; BD_UPN=12314753; BDSFRCVID=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=24ag8hak01200g8g258k245p1i37jv21n; BDSFRCVID_BFESS=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; delPer=0; BD_CK_SAM=1; BAIDUID_BFESS=0409633BC907815247521A8C2EB736E6:FG=1; ZFY=HPNxgLyd18v5YB6k:A37gl1b4q:B:AN1w4peAAbJYzFS:Bg:C; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1680231528,1680578250,1680769657,1681117159; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1681117159; BDRCVFR[QzyFDk2J3v0]=mk3SLVN4HKm; B64_BOT=1; PSINO=1; baikeVisitId=0957f42d-edcf-4025-9c22-88369bfa7461; BD_HOME=1; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDRCVFR[E-fQi7m9KnT]=6i7bDAK1zwmpvVJphc8mvqV; ariaDefaultTheme=undefined; H_PS_PSSID=; H_PS_645EC=8c3edffvokmV8%2FS70gngly9NslUKXeJHJS5mcHwpq0wp7t0TJRhaFTNDj5ivIM5XN51pJkxjEtKO; COOKIE_SESSION=235_0_8_9_4_15_1_1_8_7_1_5_0_0_0_0_1681117921_0_1681181699%7C9%23857_31_1681105585%7C9; ab_sr=1.0.1_OTg0NTJmNDIwOGJhZmM2YjE0OTI1YzA5M2Y4ZWViNTBjZGM1ZGU2NjY2YjFkNDE2YWJhOWVkZTk3NzdiYzkzN2QyNWMxY2IzODE0YzRjZTM2MjQ4ZDRmY2FjYzAyZDFiMmQwNzBkMWZjN2Q5ZmZlYmFiMDQwNDJiMTVlNmI5ODdiZWNlZThmOTgyOGFmNDUwNjg4OTY3ODk1NmYzZGU4NTY2YTczNzY0Y2Y1NDkxZGNlYjdmMjdhN2U5ZWQ4ZGFi; RT="z=1&dm=baidu.com&si=432ac630-bab4-4c0b-a0fc-6a587bfe468f&ss=lgboge30&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=19i&hd=1j8',
    # }
    # 对应URL的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'Host': 'baijiahao.baidu.com',
        # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'referer': '',
        # 'Cookie':'BIDUPSID=EC6666002B7BB97BD387A45F8A26DCE0; PSTM=1588261875; BDUSS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; BDUSS_BFESS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; MCITY=-131%3A; __yjs_duid=1_8f7399597e04daa153a297b7b9dc5e701626970583238; BAIDUID=0409633BC907815247521A8C2EB736E6:FG=1; BD_UPN=12314753; BDSFRCVID=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=24ag8hak01200g8g258k245p1i37jv21n; BDSFRCVID_BFESS=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; delPer=0; BD_CK_SAM=1; BAIDUID_BFESS=0409633BC907815247521A8C2EB736E6:FG=1; ZFY=HPNxgLyd18v5YB6k:A37gl1b4q:B:AN1w4peAAbJYzFS:Bg:C; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1680231528,1680578250,1680769657,1681117159; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1681117159; BDRCVFR[QzyFDk2J3v0]=mk3SLVN4HKm; B64_BOT=1; PSINO=1; baikeVisitId=0957f42d-edcf-4025-9c22-88369bfa7461; BD_HOME=1; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDRCVFR[E-fQi7m9KnT]=6i7bDAK1zwmpvVJphc8mvqV; ariaDefaultTheme=undefined; H_PS_PSSID=; H_PS_645EC=8c3edffvokmV8%2FS70gngly9NslUKXeJHJS5mcHwpq0wp7t0TJRhaFTNDj5ivIM5XN51pJkxjEtKO; COOKIE_SESSION=235_0_8_9_4_15_1_1_8_7_1_5_0_0_0_0_1681117921_0_1681181699%7C9%23857_31_1681105585%7C9; ab_sr=1.0.1_OTg0NTJmNDIwOGJhZmM2YjE0OTI1YzA5M2Y4ZWViNTBjZGM1ZGU2NjY2YjFkNDE2YWJhOWVkZTk3NzdiYzkzN2QyNWMxY2IzODE0YzRjZTM2MjQ4ZDRmY2FjYzAyZDFiMmQwNzBkMWZjN2Q5ZmZlYmFiMDQwNDJiMTVlNmI5ODdiZWNlZThmOTgyOGFmNDUwNjg4OTY3ODk1NmYzZGU4NTY2YTczNzY0Y2Y1NDkxZGNlYjdmMjdhN2U5ZWQ4ZGFi; RT="z=1&dm=baidu.com&si=432ac630-bab4-4c0b-a0fc-6a587bfe468f&ss=lgboge30&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=19i&hd=1j8'
        # 'Cookie':'BIDUPSID=EC6666002B7BB97BD387A45F8A26DCE0; PSTM=1588261875; BDUSS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; BDUSS_BFESS=k96dnloZkYwRlQxQ3ptbWx6b0lzWXdXa05vRWEzbjF6T1plbE1pTUJNUURubTFmRUFBQUFBJCQAAAAAAAAAAAEAAAA0CRsvuvrP~sHBMzMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRRl8DEUZff; MCITY=-131%3A; __yjs_duid=1_8f7399597e04daa153a297b7b9dc5e701626970583238; BAIDUID=0409633BC907815247521A8C2EB736E6:FG=1; BDSFRCVID=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=24ag8hak01200g8g258k245p1i37jv21n; BDSFRCVID_BFESS=tfPOJexroG0iHIof-1PyuRPfr2KKvV3TDYLEOwXPsp3LGJLVcrsEEG0PtoaGdu_-ox8EogKK0mOTHvDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbA8_CPyJIK3fP36qRrqKn8tMgT22-usX2bm2hcH0KLKol6j3TJDbCuBbf5tQqOh-Drb5-Qjbfb1MRLRyP5GX5_hXNLJX65E057kQh5TtUJGSDnTDM4MXJt7DH5yKMnitIj9-pnG2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6D-j6cbjN-s-bbfHj6MsJrHbIvPVhvOy4oTj6DXeMcJKR5hHR6m3-54LnQKhlPzQ6jD3MvB-fnN0U0eLJnQaUbIB43nSxn1Qft20hkAeMtjBbQa5gFOXR7jWhk2Dq72yhoOQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDt5FjJbIqVbOsa-5fK4bNh4bqhR3H-UnLqM7QJgOZ04n-ah02jqnVhPDVDq8u5J5TKJDHW23q-DOm3UTdsDjxyMtWWh4y5M6CLtJH-2T4KKJxbn7HsnbGBIco25kkhUJiB5OLBan7LqbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ej0bjj5M-l-X5to05TIX3b7Ef-btVh7_bJ7KhUbQMt7A2-KLtGR8Lxox5t_KOpvC36bxQhFTQtnfXpOe-n7rKhc1QJOKqp5HQT3m5-4_QUOtyKryMnb4Wb3cWKJV8UbS5xOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55uetnkj_MK; delPer=0; BAIDUID_BFESS=0409633BC907815247521A8C2EB736E6:FG=1; ZFY=HPNxgLyd18v5YB6k:A37gl1b4q:B:AN1w4peAAbJYzFS:Bg:C; BDRCVFR[QzyFDk2J3v0]=mk3SLVN4HKm; PSINO=1; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDRCVFR[E-fQi7m9KnT]=6i7bDAK1zwmpvVJphc8mvqV; ariaDefaultTheme=undefined; H_PS_PSSID=; bjhStoken=61c21678cd1a16d99338eb591bb93cf6431607dfc993ea979de5bd93cb21de3f; gray=1; canary=0; Hm_lvt_f7b8c775c6c8b6a716a75df506fb72df=1681182167; Hm_lpvt_f7b8c775c6c8b6a716a75df506fb72df=1681182167; ab_sr=1.0.1_OTg0NTJmNDIwOGJhZmM2YjE0OTI1YzA5M2Y4ZWViNTBjZGM1ZGU2NjY2YjFkNDE2YWJhOWVkZTk3NzdiYzkzN2QyNWMxY2IzODE0YzRjZTM2MjQ4ZDRmY2FjYzAyZDFiMmQwNzBkMWZjN2Q5ZmZlYmFiMDQwNDJiMTVlNmI5ODdiZWNlZThmOTgyOGFmNDUwNjg4OTY3ODk1NmYzZGU4NTY2YTczNzY0Y2Y1NDkxZGNlYjdmMjdhN2U5ZWQ4ZGFi; PHPSESSID=p3see579mjkeqsf0lucvm5t660; RT="z=1&dm=baidu.com&si=432ac630-bab4-4c0b-a0fc-6a587bfe468f&ss=lgboge30&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=19i&hd=1j8"; theme=bjh; H_WISE_SIDS=219946_234020_131862_216838_213358_214797_219942_213041_204911_230288_110085_227869_236312_243706_243889_244712_240590_245412_249606_249909_247146_250738_250303_250889_251122_251426_250759_252600_249893_252580_252947_246986_251149_253044_234484_247585_253174_234295_253480_203519_253704_246822_250095_251786_253517_254071_254079_229154_253732_254323_252306_254430_254471_249982_179345_254589_254569_254261_254730_250606_254702_254683_248124_254700_254748_244957_254832_254922_252562_255045_253600_251975_253212_255289_255294_253426_255356_251443_255449_251133_255646_255713; rsv_i=3019hkptr0g9au5UiwwUS9sfkPGyycNYFYItb7fzIKgCXO3ts%2FgeLAyNZuhKtByVTv%2B3g67RIzbvenjmA5g4mv746OWNcNw; H_WISE_SIDS_BFESS=219946_234020_131862_216838_213358_214797_219942_213041_204911_230288_110085_227869_236312_243706_243889_244712_240590_245412_249606_249909_247146_250738_250303_250889_251122_251426_250759_252600_249893_252580_252947_246986_251149_253044_234484_247585_253174_234295_253480_203519_253704_246822_250095_251786_253517_254071_254079_229154_253732_254323_252306_254430_254471_249982_179345_254589_254569_254261_254730_250606_254702_254683_248124_254700_254748_244957_254832_254922_252562_255045_253600_251975_253212_255289_255294_253426_255356_251443_255449_251133_255646_255713; SE_LAUNCH=5%3A28019703_0%3A28019703'
    }
    if para:
        response = requests.get(url, params=para, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        return response.text
    else:
        print("failed to download the page")


def get_text(url):
    soup = BeautifulSoup(download_page(url))
    all_comments = soup.find_all("div", {'class': '_3ygOc lg-fl '})
    text = ''
    for comment in all_comments:
        text += comment.get_text()  # 只提取文字
    print(text)
    return text


class BaiduSpider(object):
    def __init__(self, url, start, page_num, writer2csv, keyword):
        self.keyword = keyword
        self.url = url
        self.start = start
        self.page_num = page_num
        # urllist对应的浏览器驱动
        # 打开浏览器窗口
        # self.urllist_browser = webdriver.Chrome()
        # 不打开浏览器窗口
        self.urllist_browser = get_chrome_browser()
        # self.detail_browser = get_chrome_browser()
        self.writer2csv = writer2csv
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
        url = self.urllist_browser.current_url
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

    # 模拟进入首页
    def get_first_page(self):
        self.urllist_browser.get(self.url)
        # self.driver.find_element(value="ww").send_keys('CEO辞职')
        # self.driver.find_element(value="s_btn_wr").click()
        time.sleep(2)

    # 解析页面,写入文件
    def parse_page(self, pn):
        response = self.urllist_browser.page_source
        # 保存url list页
        with open(os.path.join(project_path, 'baijiahao', keyword + '-' + str(pn) + '.html'), 'w',
                  encoding='utf-8') as f:
            f.write(response)
        soup = BeautifulSoup(response, 'html.parser')
        hrefs = []
        # browser = webdriver.Chrome()
        browser = get_chrome_browser()
        for i, element in enumerate(soup.find_all('div', class_='result-op c-container xpath-log new-pmd')):
            title = element.h3.a.attrs['aria-label'].strip()[3:]
            href = element.h3.a.attrs['href']
            hrefs.append(href)
            abstract = element.find('span', class_='c-font-normal c-color-text').attrs['aria-label'].strip()[3:-11]
            source = element.find('span', class_='c-color-gray').attrs['aria-label'][5:]
            publish_time = None
            if element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall'):
                publish_time = element.find('span', class_='c-color-gray2 c-font-normal c-gap-right-xsmall').attrs[
                                   'aria-label'].strip()[4:]

            # 获取正文
            browser.get(href)
            # 获取网页源码
            content = browser.page_source
            # 保存为html：
            # 4.保存HTML文件
            try:
                # FIXME:标题无法做名字，因为有特殊字符
                with open(os.path.join(project_path, 'baijiahao', keyword + '-' + str(pn) + '-' + str(i) + '.html'),
                          'w',
                          encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print('文件名错误')

            soup = BeautifulSoup(content, 'html.parser')
            all_comments = soup.find_all("div", {'class': '_3ygOc lg-fl'})
            text = ''
            for comment in all_comments:
                text += comment.get_text()  # 只提取文字
            # 打印url
            # print(browser.current_url)
            # browser.switch_to.window(browser.window_handles[-1])
            browser.implicitly_wait(2)
            dic = {
                '标题': title,
                '新闻来源': source,
                '发布时间': publish_time,
                '摘要': abstract,
                '第n页': pn,
                '第n条': i,
                '链接': href,
                '正文': text
            }

            self.writer2csv.writerow(dic)  # 将数据输入到csv文件中

        # html = etree.HTML(response)
        # hrefs = html.xpath('//div[@class="result c-container "]/h3[@class="t"]/a/@href')
        # flag = html.xpath('//div[@id="page"]/a[last()]/@class')[0]
        # TODO 处理最后一页
        flag = 'n'
        return flag, hrefs

    # 点击下一页, 感觉显示、隐式等待是个摆设，所以自己封装了个等待。
    # 其实可以使用retring模块，重发几次再报错休眠，人为处理
    def click_next_page(self):
        try:
            # self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()
            # self.driver.find_element(by=By.XPATH, value="//a[@class='n']").click()
            # self.driver.find_element(by=By.XPATH, value='//div[@id="page"]/a[last()]').click()
            self.urllist_browser.find_element(by=By.PARTIAL_LINK_TEXT, value='下一页').click()
        except:
            time.sleep(10)
            # # self.driver.find_element_by_xpath('//div[@id="page"]/a[last()]').click()
            # self.driver.find_element(by=By.XPATH, value="//a[@class='n']").click()
            # self.driver.find_element(by=By.XPATH, value='//div[@id="page"]/a[last()]').click()
            self.urllist_browser.find_element(by=By.PARTIAL_LINK_TEXT, value='下一页').click()

    # 获取每一页数据, 开爬.
    def get_page_html(self):
        self.get_first_page()
        count = 0
        while True:
            page_url = self.urllist_browser.current_url
            # 获取当前页面
            pn = int(int(re.search('&pn=(\d+)', page_url).group(1)) / 10)
            # 判断是否爬取够要求页数
            if pn < self.page_num:
                print('正在处理列表页：', page_url)
                # print('解析页面：', pn, '/', self.page_num)
                flag, urls = self.parse_page(pn=pn * 10)
                count += len(urls)
                # 将详情页URL加入队列
                for url in urls:
                    self.q.put(url)
                # 判断是否为末页
                if flag != 'n':
                    print('已爬取百度全部数据')
                    break
                # 跳转至下一页 不想写显示等待，网不太好感觉还是会报错
                time.sleep(3)
                self.click_next_page()
            else:
                # self.click_next_page()
                print('爬取完毕')
                break
        print('{}共{}页{}条'.format(self.keyword, self.page_num, count))

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
        self.get_page_html()
        self.urllist_browser.close()
        # c = threading.Thread(target=self.get_page_html)
        # c.start()
        # 解析详情页
        # t = threading.Thread(target=self.get_detail_html)
        # t.start()


if __name__ == '__main__':
    # get_text(url='https://baijiahao.baidu.com/s?id=1762318451006835630&wfr=spider&for=pc')
    #
    # exit()
    # TODO：从详情页拿时间和来源更准
    keywords = [
        # '流动性困难',
        # '资金链断裂',
        # '供应链中断'，
        # '违规担保',

        # '担保违约',
        # '债务风险',
        # '债务违约',
        # '抽贷',
        # '贷款被清查',
        # '断贷',
        # '停止提供贷款',
        # '委托贷款逾期',
        # '债务清理',
        # '遭做空',
        '冻结封查',
        # '税务黑名单',
        # '财务造假',
        # '处罚',
        # '审计所被处罚',
        '内幕交易',
        '批评警示',

        '欠息',
        # '欠薪',
        # '欠税',

        # '涉黑',
        # '失信被执行人',
        # '违规借贷',
        # '违规举债',
        '违规买卖股份',
        '违规披露',
        # '违规业务',
        '机构踩雷',
        # '弹劾领导人',
        # '美伊局势',
        # '被公诉',
        # '被控制',
        # '实控人出逃',
        # '实控人涉嫌犯罪',
        # '实控人失联',
        # '实际控制人失去控制权',
        # '实控人破产',
        # '实控人死亡',
        # '实控人自杀',
        # '实控人违法',
        # '实控人严重违纪'
    ]


    # start = input('请输入开始爬取的页数：')
    # page_num = input('请输入总共爬取的页数：')
    start = 0
    page_num = 5
    search_source = '百度资讯-百家号'
    for keyword in keywords:
        # 百度首页
        # url = 'https://www.baidu.com/'
        # 百度资讯
        # url = 'https://news.baidu.com/'
        # 百度资讯+关键词+按时间+百家号
        # rrt：1 按焦点排序（默认），4 按时间排序（倒排）
        # medium：0 全部资讯（默认），1 媒体网站，2 百家号
        # 媒体网站（比较官方）：html格式差别大
        # 百家号（含大量自媒体）：html格式比较统一
        # 数量上:百家号和媒体网站 相当，一般略小于全部咨询（感知90%+），猜测百家号和媒体网站有交叉；
        url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={keyword}&medium=2&pn={start}'.format(
            keyword=keyword, start=start * 10)
        baidu = BaiduSpider(url=url, start=start, page_num=page_num, writer2csv=writer2csv(keyword), keyword=keyword)
        baidu.run()

    # driver.find_element('id', 'kw').clear()  # 清空输入框，防止下次输入的时候会连着上一次的，最后导致所有关键字都在输入框中了 driver.quit() #关闭浏览器
