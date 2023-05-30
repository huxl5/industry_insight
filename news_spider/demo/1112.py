#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 16:10 
# @Author : huxiaoliang
# @Description : 
# @See：

import requests
import json

#Diffbot API
url = 'https://api.diffbot.com/v3/article'
params = {
    'token': '044caf0e1032de57a9e4b83e37154f98',
    'url': 'https://mil.news.sina.com.cn/2020-05-22/doc-iirczymk2930805.shtml',
}
response = requests.get(url, params=params)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))