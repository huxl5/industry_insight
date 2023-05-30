#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/4 10:26 
# @Author : Eden.hu
# @description :beautifulsoap解析请求（注意乱码解决）
# @see：

import requests
from bs4 import BeautifulSoup

headers = {
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
res = requests.get('http://www.baidu.com')
# 乱码
res.encoding = 'utf8'
print(res.text)
soup = BeautifulSoup(res.text,'html.parser')   # 对返回的结果进行解析
print (soup.prettify())
