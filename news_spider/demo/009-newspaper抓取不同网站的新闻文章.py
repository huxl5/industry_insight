#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 15:29 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/weixin_43335187/article/details/85279536?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-85279536-blog-125336901.235%5Ev28%5Epc_relevant_t0_download&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-85279536-blog-125336901.235%5Ev28%5Epc_relevant_t0_download&utm_relevant_index=2

from  newspaper import Article

urls = [
'http://www.sohu.com/a/284738650_162522?_f=index_chan08news_10',
'https://view.inews.qq.com/q/20230406A03NR600?refer=wx_hot&web_channel=detail',
'https://baijiahao.baidu.com/s?id=1760983688405453371&wfr=spider&for=pc',
'https://business.sohu.com/a/660429271_121329844',
'https://new.qq.com/rain/a/20230406A08XAO00',
'https://baijiahao.baidu.com/s?id=1761793759278430173&wfr=spider&for=pc',
'http://finance.sina.com.cn/7x24/2023-04-05/doc-imypimnc2546151.shtml',
'https://baijiahao.baidu.com/s?id=1762500994815603971&wfr=spider&for=pc',
'https://news.zhibo8.cc/zuqiu/2023-04-05/642ce7f6d0875.htm',
'https://www.yicai.com/news/101723720.html',
'https://cj.sina.com.cn/articles/view/2090512390/7c9ab00602002710y',
'https://baijiahao.baidu.com/s?id=1760968774829747605&wfr=spider&for=pc',
'https://www.caixin.com/2023-03-22/102011148.html',
'https://www.163.com/dy/article/I1F3L1RD05199N88.html',
'https://finance.eastmoney.com/a/202304062684349075.html',
'https://baijiahao.baidu.com/s?id=1760969308714792328&wfr=spider&for=pc',
'http://stock.10jqka.com.cn/20230321/c645721660.shtml',
'http://sc.stock.cnfol.com/ggzixun/20201217/28595401.shtml'

]

#这里的url可以填写你需要爬取的网址
for url in urls:
    news = Article(url,language = 'zh')
    news.download()
    news.parse()

    print(news.url.strip())
    #news.url为获取网址的url
    print(news.text.strip().replace(' ','').replace('   ',''))
    # news.text为获取页面的所有text文字
    print(news.title.strip())
    # news.title为获取页面的所有标题
    # print(news.html)
    # news.html为获取页面的所有源码
    # print(news.authors)
    # print(news.top_image)
    # print(news.movies)
    # print(news.keywords)
    # print(news.summary)
    print('='*50)
    # print(news.images)
    # print(news.imgs)
