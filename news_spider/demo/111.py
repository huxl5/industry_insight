#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 9:02 
# @Author : huxiaoliang
# @Description : 
# @See：

import requests
import re
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}


def baidu(keyword, page):  # 定义函数，方便之后批量调用
    num = (page - 1) * 10
    # url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + keyword + '&pn=' + str(num)
    url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd={}&tn=news&rsv_bp=1&oq=&rsv_btype=t&f=8&x_bfe_rqs=032000000000000000000000000000000000000000000008&x_bfe_tjscore=0.080000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn={}'.format(
        keyword, num)
    print(url)
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    res = res.text  # 通过requests库爬虫

    # 2.  获取信息的网址和标题
    # 获取信息的网址
    p_href = '<h3 class="news-title_1YtI1 "><a href="(.*?)"'
    href = re.findall(p_href, res)
    print(href)

    # 获取信息的标题
    p_title = '<h3 class="news-title_1YtI1 ">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    print(title)

    # 3. 获取信息的来源和日期
    # 获取信息的来源
    p_source = '<span class="c-color-gray" aria-label=.*?>(.*?)</span>'
    source = re.findall(p_source, res)
    print(source)

    # 获取信息的日期
    p_date = '<span class="c-color-gray2 c-font-normal c-gap-right-xsmall" aria-label=".*?>(.*?)</span>'
    date = re.findall(p_date, res)
    print(date)

    # # 获取信息的摘要和正文
    #
    # # 数据清洗
    # source = []
    # date = []
    # for i in range(len(title)):
    #     title[i] = title[i].strip()
    #     title[i] = re.sub('<.*?>', '', title[i])
    #     info[i] = re.sub('<.*?>', '', info[i])
    #     source.append(info[i].split('&nbsp;&nbsp;')[0])
    #     date.append(info[i].split('&nbsp;&nbsp;')[1])
    #     source[i] = source[i].strip()
    #     date[i] = date[i].strip()
    #
    # # 通过字典生成二维DataFrame表格
    # result = pd.DataFrame({'关键词': keyword, '标题': title, '网址': href, '来源': source, '日期': date})
    # return result


print(baidu('CEO辞职', 1))
# 通过pandas库将数据进行整合并导出为Excel

#
# df = pd.DataFrame()
#
# keywords = ['华能信托', '人工智能', '科技', '体育', 'Python', '娱乐', '文化', '阿里巴巴', '腾讯', '京东']
# for keyword in keywords:
#     for i in range(10):  # 循环10遍，获取10页的信息
#         result = baidu(keyword, i + 1)
#         df = df.append(result)  # 通过append()函数添加每条信息到df中
#         print(keyword + '第' + str(i + 1) + '页爬取成功')
#
# df.to_excel('新闻_new.xlsx')  # 在代码所在文件夹生成EXCEL文件
