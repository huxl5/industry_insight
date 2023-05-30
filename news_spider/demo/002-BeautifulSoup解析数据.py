#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/4 10:26 
# @Author : Eden.hu
# @description :
# @see：https://www.cnblogs.com/awesometang/p/11991755.html
'''
1、合法协议：robots.txt。eg：https://www.taobao.com/robots.txt
2、语言：python开发效率高，执行效率不高，但瓶颈是IO，python优秀的库多，requests，beautifulsoap,selenium
3、# 对于特定类型请求，如Ajax请求返回的json数据：res.json()
4、# post请求
data = {'users': 'abc', 'password': '123'}
r = requests.post('https://www.weibo.com', data=data, headers=headers)
5、避免多次登陆，保持一个回话
# 保持会话
# 新建一个session对象
sess = requests.session()
# 先完成登录
sess.post('maybe a login url', data=data, headers=headers)
# 然后再在这个会话下去访问其他的网址
sess.get('other urls')
6、beautifulsoup：方便解析源码
通过标签+属性的方式来进行定位，譬如说我们想要百度的logo
eg：demo可看
7、拉钩，post，ajax，json数据demo

'''


# TODO：
import requests


class Config:
    kd = '数据分析'
    referer = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput='
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


class Spider:

    def __init__(self, kd=Config.kd):
        self.kd = kd
        self.url = Config.referer
        self.api = 'https://www.lagou.com/jobs/positionAjax.json'

        # 必须先请求referer网址
        self.sess = requests.session()
        self.sess.get(self.url, headers=Config.headers)

    def get_position(self, pn):
        data = {'first': 'true',
                'pn': str(pn),
                'kd': self.kd
                }
        # 向API发起POST请求
        r = self.sess.post(self.api, headers=Config.headers, data=data)

        # 直接.json()解析数据
        return r.json()['content']['positionResult']['result']

    def engine(self, total_pn):
        for pn in range(1, total_pn + 1):
            results = self.get_position(pn)
            for pos in results:
                print(pos['positionName'], pos['companyShortName'], pos['workYear'], pos['salary'])


if __name__ == '__main__':
    lagou = Spider()
    lagou.engine(2)
