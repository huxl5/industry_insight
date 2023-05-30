#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/27 18:38 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/weixin_56741605/article/details/128467321

# 关闭警告
import warnings

warnings.filterwarnings("ignore")

'''
由于数据量较大，建议将数据分成几组，多次爬虫，避免一次爬虫过程中，爬虫时间较长，出现意外情况而未能保存数据
'''
import requests, time, random, json
import pandas as pd


def req(stock, year, org_dict):
    # post请求地址（巨潮资讯网的那个查询框实质为该地址）
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    # url = "http://www.cninfo.com.cn/new/disclosure/query"
    # 表单数据，需要在浏览器开发者模式中查看具体格式
    data = {
        "pageNum": "1",
        "pageSize": "30",
        "tabName": "fulltext",
        "stock": stock + "," + org_dict[stock],  # 按照浏览器开发者模式中显示的参数格式构造参数
        "seDate": f"{str(int(year) + 1)}-01-01~{str(int(year) + 1)}-04-28",
        "column": "hke",# fixme：szse：沪股
        # "category": "category_ndbg_szsh",
        # "isHLtitle": "true",
        "sortName": "time",
        "sortType": "desc",
        # "plate":"hkmb;hkcy", 港主版，港创业版
        "isHLtitle": True
    }
    # 请求头
    headers = {"Content-Length": "201", "Content-Type": "application/x-www-form-urlencoded"}
    # 发起请求
    req = requests.post(url, data=data, headers=headers)

    if json.loads(req.text)["announcements"]:  # 确保json.loads(req.text)["announcements"]非空，是可迭代对象
        for item in json.loads(req.text)["announcements"]:  # 遍历announcements列表中的数据，目的是排除英文报告和报告摘要，唯一确定年度报告或者更新版
            # 全部公告
            adjunctUrl = item["adjunctUrl"]  # "finalpage/2019-04-30/1206161856.PDF" 中间部分便为年报发布日期，只需对字符切片即可
            pdfurl = "http://static.cninfo.com.cn/" + adjunctUrl
            # "secCode":"00383",
            # "secName":"中国医疗网络",
            # "orgId":"gshk0000383",
            # "announcementId":"1216674109",
            # "announcementTitle":"股东周年大会通告",
            # "announcementTime":1682611199000,
            # "adjunctUrl":"finalpage/2023-04-27/1216674109.PDF",
            pdf_name = item["secCode"]+"-"+item["orgId"]+"-"+item["secName"]+"-"+item["announcementTitle"]+".pdf"
            r = requests.get(pdfurl)
            f = open("公告" + "/" + pdf_name, "wb")
            f.write(r.content)
            # print(f"{stock}-{year}年报下载完成！")  # 打印进度
            # 年报代码
            # if "摘要" not in item["announcementTitle"]:
            #     if "英文" not in item["announcementTitle"]:
            #         if "修订" in item["announcementTitle"] or "更新" in item["announcementTitle"]:
            #             adjunctUrl = item["adjunctUrl"]  # "finalpage/2019-04-30/1206161856.PDF" 中间部分便为年报发布日期，只需对字符切片即可
            #             pdfurl = "http://static.cninfo.com.cn/" + adjunctUrl
            #             r = requests.get(pdfurl)
            #             f = open("年报" + "/" + stock + "-" + year + "年度报告" + ".pdf", "wb")
            #             f.write(r.content)
            #             print(f"{stock}-{year}年报下载完成！")  # 打印进度
            #             break
            #         else:
            #             adjunctUrl = item["adjunctUrl"]  # "finalpage/2019-04-30/1206161856.PDF" 中间部分便为年报发布日期，只需对字符切片即可
            #             pdfurl = "http://static.cninfo.com.cn/" + adjunctUrl
            #             r = requests.get(pdfurl)
            #             f = open("年报" + "/" + stock + "-" + year + "年度报告" + ".pdf", "wb")
            #             f.write(r.content)
            #             print(f"{stock}-{year}年报下载完成！")  # 打印进度
            #             break


# 该函数主要是通过http://www.cninfo.com.cn/new/data/szse_stock.json该json数据，找到每个stock对应的orgid，并存储在字典org_dict中
def get_orgid():
    org_dict = {}
    # A股
    # org_json = requests.get("http://www.cninfo.com.cn/new/data/szse_stock.json").json()["stockList"]
    org_json = requests.get("http://www.cninfo.com.cn/new/data/hke_stock.json").json()["stockList"]

    for i in range(len(org_json)):
        org_dict[org_json[i]["code"]] = org_json[i]["orgId"]

    return org_dict


if __name__ == "__main__":  # 程序入口
    # 读取需要爬取的股票代码
    # pdlist = pd.read_excel("stockcode.xlsx", converters={'stockcode': str})["stockcode"]
    # stock_list = pdlist.to_numpy().tolist()

    stock_list = ['00383']
    # stock_list = ['688553','688737']


    org_dict = get_orgid()

    for stock in stock_list:  # 一层循环，按股票代码循环
        for year in ["2023", "2022", "2021"]:  # 二层按年份循环
            req(stock, year, org_dict)  # 调用req函数
            time.sleep(random.randint(0, 2))  # 适当休眠，避免爬虫过快
