#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/19 16:10 
# @Author : huxiaoliang
# @Description : python 文件读取工具类
# @See：

# 关闭警告
import warnings

warnings.filterwarnings("ignore")
import csv
def demo():

    # CSV相关读写
    # see：http://c.biancheng.net/python_spider/csv-module.html



    # 1) csv.writer()
    # csv 模块中的 writer 类可用于读写序列化的数据，其语法格式如下：
    # 操作文件对象时，需要添加newline参数逐行写入，否则会出现空行现象
    with open('eggs.csv', 'w', newline='') as csvfile:
        # delimiter 指定分隔符，默认为逗号，这里指定为空格
        # quotechar 表示引用符
        # writerow 单行写入，列表格式传入数据
        spamwriter = csv.writer(csvfile, delimiter=' ')
        spamwriter.writerow(['www.biancheng.net'] * 5 + ['how are you'])
        spamwriter.writerow(['hello world', 'web site', 'www.biancheng.net'])

    # 2）csv.DictWriter()
    # 当然也可使用 DictWriter 类以字典的形式读写数据，使用示例如下：
    with open('names.csv', 'w', newline='') as csvfile:
        #构建字段名称，也就是key
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入字段名，当做表头
        writer.writeheader()
        # 多行写入
        writer.writerows([{'first_name': 'Baked', 'last_name': 'Beans'},{'first_name': 'Lovely', 'last_name': 'Spam'}])
        # 单行写入
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


    with open('eggs.csv', 'r', newline='') as csvfile:
        # todo:quotechar的作用
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['first_name'], row['last_name'])


def output_csv(datalist, keyword, search_source):
    csv_file = open("xueqiu/{}.csv".format(keyword), 'w', newline='',
                    encoding='utf')  # 解决中文乱码问题。a+表示向csv文件追加,w直接写入;utf-8-sig;
    writer = csv.writer(csv_file, delimiter='`')
    writer.writerow(['标题', '新闻来源', '发布时间', '摘要', '第n页', '第n条', '链接', '正文'])
    for data in datalist:
        writer.writerow(
            [data['title'], data['source'], data['time'], data['abstract'], data['page'], data['num'], data['target'],
             data['text'], ])
    csv_file.close()

if __name__ == '__main__':
    demo()

