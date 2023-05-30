#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 9:14 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/m0_51952698/article/details/118613836

# 关闭警告
import warnings

warnings.filterwarnings("ignore")

import csv
import json
import re
import os

import requests
from bs4 import BeautifulSoup
import platform

curr_dir = os.getcwd()
print(curr_dir)
if platform.system().lower() == 'windows':
    project_path = r'D:\work_softs\workspace-py-citic\industry_insight\news_spider'
elif platform.system().lower() == 'linux':
    project_path = '/root/projects'


def download_page(url, i, j, para=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}
    if para:
        response = requests.get(url, params=para, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        # 4.保存HTML文件
        with open(os.path.join(project_path, 'xueqiu', keyword + '-' + str(i) + '-' + str(j) + '.html'), 'w',
                  encoding='utf-8') as f:
            f.write(response.text)
        return response.text
    else:
        print("failed to download the page")


def xueqiu(start, end, keyword):
    # 将响应头的参数补齐以避免无法读取的情况
    headers = {
        "Referer": "https://xueqiu.com/k?q=",
        "Host": "xueqiu.com",
        "Cookie": "device_id=7a080e5fb9772ae0ea18c91666ffb7e6; s=d4112md9rh; __utmz=1.1680240929.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1680139153,1680588511; __utma=1.419170359.1680240929.1680240929.1680830133.2; __utmc=1; remember=1; xq_a_token=5948d36c0f07750d7819f2fc255c0699d82d6461; xqat=5948d36c0f07750d7819f2fc255c0699d82d6461; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjI0ODA4ODY0NjEsImlzcyI6InVjIiwiZXhwIjoxNjgzNDIyMjA2LCJjdG0iOjE2ODA4MzAyMDYyNDUsImNpZCI6ImQ5ZDBuNEFadXAifQ.Xny2yNyGw0USYlfs9oKsxTe_DqjLGD6tkVTTbI0Fm7EQn_L1fBBwHVo92Cm-6tp-IZtOWdiAAtTeiuVVXjLIYcxqFFUVvzTZp_XeCzcXnbwboE1QsOPuiaf0ye6BVZIAN-8aKtXdh-GP-FWpDHcjX3gt76jVfAridv1Kck67gciaYeoPEaC7O-iz6vv8KpRiU60of_zZ4rgcArJAYNWJA36mdSbl_pimeTXJbKbl6PSV7AkJMY_0v_YQs-86sI8JGC65AXOA3OnFeqA6TuwcWQUp3SGJibuCntp0nv0gXXvqpvyDNRdKKxvHdVp3pNcYx-V8DEiZjFGy728IS1ge3w; xq_r_token=3e1ede81b4a76e05c8e74544bbe242436001e13b; xq_is_login=1; u=2480886461; snbim_minify=true; acw_tc=2760827216808320097005961e4a692ecc9fbc9bc3a02a5ef989d4b5a44a7e; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1680832052",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}
    comments_list = []
    # 遍历每一页的URL
    for i in range(int(start), int(end) + 1):
        # fixme：sortId=1：默认排序；sortId=2：按最新评论；sortId=3：评论最多；
        url = 'https://xueqiu.com/query/v1/search/status.json?sortId=2&q={keyword}&count=10&page='.format(
            keyword=keyword) + str(i)
        print('正在处理列表页：', url)  # 用于检查
        response = requests.get(url, headers=headers, verify=False, timeout=30)  # 禁止重定向
        response.encoding = response.apparent_encoding
        content = response.text
        if response.status_code == 200:
            # 4.保存HTML文件
            with open(os.path.join(project_path, 'xueqiu', keyword + '-' + str(i) + '.html'), 'w',
                      encoding='utf-8') as f:
                f.write(response.text)
        else:
            print("failed to download the page")
        # 读取的是json文件。因此就用json打开啦
        result = json.loads(content)
        # 找到原始页面中数据所在地
        comments = result['list']
        for j in range(0, len(comments)):
            # TODO:+摘要，新闻来源，引擎；列表排序方式指定
            comment = {}
            # 取出需要的字段并存入字典中
            comment['title'] = re.sub(r"<span class='highlight'>.*?</span>", '', comments[j]['title'])
            comment['source'] = comments[j]['source']
            comment['time'] = comments[j]['timeBefore']
            # 从初始页面获取内容的链接（不全，需要自行补齐），直接调用自己的方法读取文本内容
            comment['abstract'] = re.sub(r"<span class='highlight'>.*?</span>", '', comments[j]['description'])
            comment['target'] = "https://xueqiu.com" + comments[j]['target']
            text = get_text(comment['target'], i, j)
            text = re.sub(r"<span class='highlight'>.*?</span>", '', text)
            res = re.search(r"来源：.*?）", text)
            if res:
                text = re.sub(r"来源：.*?）", '', text)
                comment['author'] = re.search(r'作者：.*?，（', res.group()).group()[3:-2].strip()
                comment['source'] = re.search(r'来源：.*?，', res.group()).group()[3:-1].strip()
            comment['text'] = text
            comment['page'] = i
            comment['num'] = j
            comments_list.append(comment)
    print('{}共{}页{}条'.format(keyword, end - start + 1, len(comments_list)))
    return comments_list


def get_text(url, i, j):
    soup = BeautifulSoup(download_page(url, i, j))
    pattern = re.compile("article__bd__detail.*?")  # 按标签寻找
    all_comments = soup.find_all("div", {'class': pattern})
    text1 = all_comments[0]
    con = text1.get_text()  # 只提取文字
    return con


def output_csv(datalist, keyword, search_source):
    csv_file = open(os.path.join(project_path, "xueqiu/{}.csv".format(keyword)), 'w', newline='',
                    encoding='utf')  # 解决中文乱码问题。a+表示向csv文件追加,w直接写入;utf-8-sig;
    writer = csv.writer(csv_file, delimiter='`')
    writer.writerow(['标题', '新闻来源', '发布时间', '摘要', '第n页', '第n条', '链接', '正文'])
    for data in datalist:
        writer.writerow(
            [data['title'], data['source'], data['time'], data['abstract'], data['page'], data['num'], data['target'],
             data['text'], ])
    csv_file.close()


if __name__ == "__main__":
    keywords = [
        '流动性困难',
        '资金链断裂',
        '供应链中断',
        '违规担保',
        '担保违约',
        # '"担保违约"',
        # '债务风险',
        # '债务违约'


        # 'CEO辞职',
        # '董事长辞职',
        # '高管辞职',
        # '总裁辞职',
        # '董秘辞职',
        # '董事辞职'
    ]
    # start = input('请输入开始爬取的页数：')
    # end = input('请输入结束爬取的页数：')
    start = 1
    end = 5
    search_source = 'xueqiu'
    for keyword in keywords:
        result = xueqiu(start, end, keyword)
        output_csv(result, keyword, search_source)

