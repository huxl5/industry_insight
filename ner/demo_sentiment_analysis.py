#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/8 16:13 
# @Author : huxiaoliang
# @Description : 
# @See：

# 关闭警告
import warnings
from hanlp_restful import HanLPClient

warnings.filterwarnings("ignore")

# 创建客户端，填入服务器地址和秘钥：
url = 'https://www.hanlp.com/api'
HanLP = HanLPClient(url, auth='MjMzNkBiYnMuaGFubHAuY29tOjVPaGpUeUI2VkJBVzR6Vmo=', language='zh')
text = '''“这是一部男人必看的电影。”人人都这么说。但单纯从性别区分，就会让这电影变狭隘。
《肖申克的救赎》突破了男人电影的局限，通篇几乎充满令人难以置信的温馨基调，而电影里最伟大的主题是“希望”。
当我们无奈地遇到了如同肖申克一般囚禁了心灵自由的那种囹圄，我们是无奈的老布鲁克，灰心的瑞德，还是智慧的安迪？
运用智慧，信任希望，并且勇敢面对恐惧心理，去打败它？
经典的电影之所以经典，因为他们都在做同一件事——让你从不同的角度来欣赏希望的美好。'''
print(HanLP.sentiment_analysis(text))
