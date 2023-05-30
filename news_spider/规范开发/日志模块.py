#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/12 8:55 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/Ces222/article/details/127186508

# 关闭警告
# import warnings
#
# warnings.filterwarnings("ignore")

import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.DEBUG)
#
# # 设置日志的格式
# formatter = logging.Formatter('%(asctime)s – %(filename)s[line:%(lineno)d] – %(levelname)s: %(message)s')
#
# # 创建一个控制台输出的日志对象
# console = logging.StreamHandler()
# console.setFormatter(formatter)
# logger.addHandler(console)
# logger.debug('—–调试信息[debug]—–')
#
# logger.info('—–有用的信息[info]—–')
#
# logger.warning('—–警告信息[warning]—–')
#
# logger.error('—–错误信息[error]—–')
#
# logging.critical('—–严重错误信息[critical]—–')
#
# logger.info('='*50)
import os

# 设置日志路径
current_path = os.path.dirname(__file__)
log_path = os.path.join(current_path, './logs/test.log')
# 创建logger日志对象
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('file:%(asctime)s – %(filename)s[line:%(lineno)d] – %(levelname)s: %(message)s')
# 创建一个文件输出的日志对象
file_log = logging.FileHandler(log_path, encoding='utf-8')
# 设置日志格式
file_log.setFormatter(formatter)
# 把文件输出的日志对象 传给logger日志对象
logger.addHandler(file_log)
logger.debug('—–调试信息[debug]—–')
logger.info('—–有用的信息[info]—–')
logger.warning('—–警告信息[warning]—–')
logger.error('—–错误信息[error]—–')
logger.critical('—–严重错误信息[critical]—–')

logger.info('Hello word!!!')
