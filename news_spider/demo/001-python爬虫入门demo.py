#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/3 15:53 
# @Author : huxiaoliang
# @description :
# @see:https://blog.csdn.net/weixin_44940488/article/details/117788963
# @for：理解爬虫入门demo
'''
1、python通过requet.get(url).text 获取源代码-浏览器不同意
2、设置代理，requet.get(url,headers={'User-Agent':'Mozilla/5.0...'}).text
3、分析源码的方法：F12；右击选择“查看网页源代码”；在Python获得的网页源代码中查看：.res.text
'''

import requests   # 导入requests库
import re # 导入正则库

# 1.  获取网页源代码
# 尝试一：python请求
# url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'  # 输入网址
# # url = 'http://www.baidu.com'
# res = requests.get(url).text    # 发送请求获取网页
# print(res)    # 输出网页源码

# exit()
# 尝试二：用户代理设置,模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}

# 三种url均可，第四种是带page
# url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'
# url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=阿里巴巴'
# url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4&tn=news&rsv_bp=1&rsv_sug3=1&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&oq=&rsv_btype=t&f=8&inputT=3&rsv_sug4=971&rsv_sug=1&x_bfe_rqs=032000000000000000000000000000000000000000000008&x_bfe_tjscore=0.080000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn=10'

#如果遇到抛出异常，修改后爬虫程序还需要再重新运行，效率很低。这时可以使用try来避免异常
try:
    #Requsets 库不仅有get()方法，还有post()等方法，用来提交表单来爬取需要登陆才能获取数据的网络。
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    res = res.text  # 通过requests库爬虫
    print(res)
except ConnectionError:#出现except后面的错误后执行下面聚聚
    print('拒绝连接')

# exit()
# print(res)
# res.encoding = 'utf8'
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

# 获取信息的摘要和正文



# 4.  数据清洗和打印输出
# 数据清洗和打印输出 # FIXME：10条取到7条，后三条不知为啥了：原因：有的时间没有
for i in range(len(title)):  # range(len(title)),这里因为知道len(title) = 10，所以也可以写成for i in range(10)
    title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过这里好像不太需要了
    title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
    print(str(i + 1) + '.' + title[i], source[i],date[i],href[i])  # print(1, 'hello') 这种写法，就是在同一行连续打印多个内容
    # print(str(i + 1) + '.' + title[i] + ' ' + source[i] + ' ' + date[i])  # 这个是纯字符串拼接
    # print(href[i])   # 输出链接




exit()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'  # 把链接中rtt参数换成4即是按时间排序，默认为1按焦点排序
url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
res = requests.get(url, headers=headers).text  # 加上headers用来告诉网站这是通过一个浏览器进行的访问



"""使用正则表达式提取信息"""
# 获取信息的链接
p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
href = re.findall(p_href, res)

# 获取信息的标题
p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)

# 获取信息的来源
p_source = '<span class="c-color-gray c-font-normal c-gap-right" aria-label=.*?>(.*?)</span>'
source = re.findall(p_source, res)

# 获取信息的日期
p_date = '<span class="c-color-gray2 c-font-normal" aria-label=".*?>(.*?)</span>'
date = re.findall(p_date, res)

for i in range(len(title)):  # range(len(title)),这里因为知道len(title) = 10，所以也可以写成for i in range(10)
    title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过这里好像不太需要了
    title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
    print(str(i + 1) + '.' + title[i], source[i], date[i])  # print(1, 'hello') 这种写法，就是在同一行连续打印多个内容
    # print(str(i + 1) + '.' + title[i] + ' ' + source[i] + ' ' + date[i])  # 这个是纯字符串拼接
    print(href[i])  # 输出链接