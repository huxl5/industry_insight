#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/19 15:25
# @Author : huxiaoliang
# @Description : 对资讯信息进行组织机构识别
# @See：



# 关闭警告
import warnings

import csv
from hanlp_restful import HanLPClient

warnings.filterwarnings("ignore")
# 创建客户端，填入服务器地址和秘钥：
url = 'https://www.hanlp.com/api'
HanLP = HanLPClient(url, auth='MjMzNkBiYnMuaGFubHAuY29tOjVPaGpUeUI2VkJBVzR6Vmo=', language='zh')
# res =HanLP('我在上海林原科技有限公司兼职工作，我经常在台川喜宴餐厅吃饭，偶尔去开元地中海影城看电影。', tasks='ner/msra')
# print(res)
def is_ORGANIZATION(val):
    if val[1]=='ORGANIZATION':
        return True
    else:
        return False
# rts=list(filter(is_ORGANIZATION,res['ner/msra']))
#
# print(res['ner/msra'],type(res['ner/msra']),rts,sep='\n')
# exit()


# 读取数据
# todo: 绝对路径-》相对路径
# with open(r'D:\work_softs\workspace-py-citic\industry_insight\news_spider\xueqiu\CEO辞职.csv', 'r', newline='',encoding='utf-8') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter='`')
#     for row in spamreader:
#         print('`'.join(row))

# writer.writerow(['标题', '新闻来源', '发布时间', '摘要', '第n页', '第n条', '链接', '正文'])
with open(r'D:\work_softs\workspace-py-citic\industry_insight\news_spider\xueqiu\CEO辞职.csv', 'r', newline='',
          encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='`')
    for row in reader:
        print(row['标题'], row['摘要'], row['正文'], sep='\n')
        print('=' * 100)
        #
        # 对正文识别组织机构
        # fixme：先切分句子，对每个句子ner提取：ress为三维数组；
        ress = HanLP(row['正文'], tasks='ner/msra')['ner/msra']
        print(ress)
        # fixme：res为每个句子ner提取结果，二维数组
        for res in ress:
            rts = list(filter(is_ORGANIZATION, res))
            if rts:
                print( rts, sep='\n')


