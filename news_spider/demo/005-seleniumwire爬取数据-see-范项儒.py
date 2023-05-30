#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/3 15:33 
# @Author : huxiaoliang
# @description :
import requests
# todo1, 开chrome后台版，提前session， 运行程序，关闭chrome
from seleniumwire import webdriver
import pickle
import time
import os
import joblib
# os.environ['PATH']='/opt/google/chrome:'+os.environ['PATH']
driver = webdriver.Chrome()

# export_data = {'location':location_dic,'path':'path_string',''}# 最小单元定义为位置一致的最大parent
# Step 1: js locate all minimum element with size >0
# export all_these out, together with innerText & path
# Step 2: python adding feature to all these elements. Tag+lenght+encoding+sensitive word
# Step 3: regression model to export result. (2 MODELS./////////////////////////////////////////////////////////////////////////// 1 for title, 1 for content)
# Step 4: return predicted element
# step 5: find element's parent, then located href.

js1 = """
var node = document.body;
parent_path = 0
function get_all_elem(node,parent_path){
    console.log(node.tagName)
    var infos = []
    var i;
    var c = node.children
    for (i = 0; i < c.length; i++) {
        item = c[i]
        // console.log(i)
        box = c[i].getBoundingClientRect();
        if (box.width*box.height>0){
            info = {}
            info['box']= box
            info['text']=item.innerText

            info['path']=parent_path+','+i
            console.log(info['box'])
            console.log(info['path'])
            info['child_num'] = item.childElementCount
            info['outerHTML'] = item.outerHTML
            info['tagname'] = item.tagName
            info['attributes'] = item.attributes
            // console.log(info)

            infos = infos.concat(info)
            var childs = get_all_elem(item,info['path'])
            console.log('finsh recurse')
            infos = infos.concat(childs)
            }
        console.log('continue loop'+i+' '+c.length)
        }
    console.log('return')
    return infos
}
all_body_elem = get_all_elem(node,parent_path)
return all_body_elem
"""
# driver.get('http://www.nbd.com.cn/')
# driver.get('http://search.ccgp.gov.cn/bxsearch')
# driver.get('https://www.163.com/')

driver.set_page_load_timeout(30)

def get_web_info(site):
    tmp_return = []
    driver.get(site)
    all_node = driver.execute_script(js1)
    feature = []
    import pandas as pd
    import re
    from bs4 import BeautifulSoup
    for node in all_node:
        out_html = node['outerHTML']
        if ('<a' in out_html) and ('href' in out_html):
            try:
                tmp = BeautifulSoup(node['outerHTML'])
                href = tmp.find('a').attrs['href']
            except:
                href = ''
        else:
            href = ''
        node['href'] = href
        tag_is_a = int(node['tagname'] == 'A')
        feature_dic = {'num_text': len(node['text'].strip()),
                       'width_height_ratio': node['box']['width'] / node['box']['height'],
                       'child_node': node['child_num'],
                       'len_href': len(href),
                       'tag_is_a': tag_is_a,
                       'x_pst': node['box']['top']
                       }
        feature.append(feature_dic)
    feature_df = pd.DataFrame(feature)

    def model(feature):
        s1 = (feature['num_text'] < 40).astype('int')
        s2 = (feature['width_height_ratio'] > 1).astype('int')
        s3 = (feature['child_node'] == 0).astype('int')
        s4 = (feature['len_href'] > 0).astype('int')
        s5 = (feature['x_pst'] < 2080).astype('int')
        s6 = (feature['num_text'] > 10).astype('int')
        score = s4 + s5 + s2 + s6 + s3 + s1  # s1.astype('int')+s2+s3.astype('int')+s4.astype('int')+s5.astype('int')+s6.astype('int')
        return score

    score = model(feature_df)
    feature_df['score'] = score
    feature_df['text'] = [node['text'] for node in all_node]
    import numpy as np

    idxes = np.where(score == 6)
    for id, idx in enumerate(idxes[0]):
        info = web.copy()
        info['text'] = all_node[idx]['text']
        info['href'] = all_node[idx]['href']
        print(f'{id}:', all_node[idx]['text'],'href：',all_node[idx]['href'])
        tmp_return.append(info)
    return tmp_return
web = {'name':'网易','site':'https://www.163.com/'}
# web = {'name':'百度','site':'https://www.baidu.com/'}
# web = {'name':'百度新闻','site':'https://news.baidu.com/'}
# web = {'name':'百度新闻','site':'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=CEO%E8%BE%9E%E8%81%8C'}

if __name__ == '__main__':

    get_web_info(web['site'])
    '''
    Q1：web对象的写法对吗
    Q2：似乎爬取列表页的，但是输入关键字后失败
    
    '''
    # 加载某文件
    # all_web = joblib.load('info2export')
    # 文件转换为dict
    # all_web = all_web.to_dict(orient='records')
    # result2return = []
    # for web in all_web:
    #     name = web['name']
    #     site= web['site']
    #     print(name, site)
    #     try:
    #
    #
    #         result_ret = get_web_info(site)
    #         result2return = result2return+result_ret
    #         # raise Exception('ag')
    #     except:
    #         print('skipping page',name, site)
    #         continue