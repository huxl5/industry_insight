#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/28 9:58 
# @Author : huxiaoliang
# @Description : 
# @See：AI

# 关闭警告
import warnings

warnings.filterwarnings("ignore")

# 以下是一个简单的爬取巨潮资讯所有港股公告的Python脚本的示例代码：
# 以上代码以POST请求方式向巨潮资讯网站查询港股公告，并通过解析JSON数据获取公告信息。本代码仅供参考，实际使用时可能需要根据需要进行扩展或修改。


import requests
from bs4 import BeautifulSoup

# 构造请求头，设置用户代理
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 构造URL，查询港股公告
url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
# url = 'http://www.cninfo.com.cn/new/disclosure'

# 构造请求参数
params = {
    'column': 'hkgg',
    'pageNum': 1,
    'pageSize': 30,
    'tabName': 'fulltext',
    'sortName': '',
    'sortType': '',
    'limit': '',
    'searchkey': ''
}

# 发送POST请求，获取数据
response = requests.post(url, headers=headers, params=params)
content = response.json()
announcements = content['announcements']

# 输出公告标题和链接
for announcement in announcements:
    print(announcement['announcementTitle'])
    print('http://www.cninfo.com.cn/' + announcement['adjunctUrl'])


