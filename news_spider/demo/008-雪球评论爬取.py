#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/7 9:14 
# @Author : huxiaoliang
# @Description : 
# @See：https://blog.csdn.net/weixin_44745159/article/details/110144603

import requests
import re
import json
import csv
import time
import datetime

# cookie替换成从自己的浏览器获取到的cookie，需要登录后再获取否则无法爬取超过5页数据
cookie = '你自己的cookie'
headers = {
    'Host':"xueqiu.com",
    'Referer': 'https://xueqiu.com/',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
    'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Connection':'keep-alive',
    'Cookie': cookie
}

# 初始化数据
page = 1
userid = 9219380043   # 这里填写你要爬取的用户UID
type = 0
url = 'https://xueqiu.com/v4/statuses/user_timeline.json'+'?page='+str(page)+'&user_id='+str(userid)+'&type='+str(type)
response = requests.get(url, headers = headers)
text = response.text
dict_text = json.loads(text)
# 获取maxPage
maxPage = dict_text['maxPage']
userName = dict_text['statuses'][0]['user']['screen_name']
csv_headers = ['id','user_id','source','title','created_at','retweet_count','reply_count','fav_count','truncated','commentid','retweet_status_id','symbol_id','description','type','source_link','edited_at','mark', 'reward', 'liked', 'quote_cards', 'rqtype', 'paid_mention', 'is_answer', 'donate_count', 'text', 'is_no_archive', 'topic_desc', 'firstImg', 'offer', 'topic_symbol', 'longTextForIOS', 'cover_pic', 'promotion_url', 'target', 'topic_pic_headOrPad', 'retweeted_status', 'like_count', 'commentId', 'status_industry', 'meta_keywords', 'is_column', 'timeBefore', 'is_bonus', 'favorited', 'recommend_cards', 'is_original_declare', 'topic_pic_thumbnail', 'score', 'is_refused', 'reward_amount', 'notice_tag', 'promotion_pic', 'excellent_comments', 'talk_count', 'show_cover_pic', 'expend', 'is_private', 'pic_sizes', 'new_card', 'rqid', 'fragment', 'topic_pic', 'rawTitle', 'stockCorrelation', 'promotion_id', 'canEdit', 'blocking', 'pic', 'blocked', 'topic_title', 'reward_user_count', 'cover_pic_size', 'reward_count', 'forbidden_retweet', 'card', 'topic_pic_thumbnail_small', 'view_count', 'reply_user_count', 'is_ss_multi_pic', 'tagStr', 'common_emotion', 'answers', 'weixin_retweet_count', 'tags', 'favorited_created_at', 'controversial', 'donate_snowcoin', 'mp_not_show_status', 'mark_desc', 'user', 'reply_user_images', 'tagsForWeb', 'order_id', 'current_stock_price', 'forbidden_comment']
last_index = 0
statuses_formatted = []
csv_headers_statuses_formatted = ['发布时间','转发数','评论数','收藏数','点赞数','动态内容']
for page in range(1,maxPage+1):
    url = 'https://xueqiu.com/v4/statuses/user_timeline.json'+'?page='+str(page)+'&user_id='+str(userid)+'&type='+str(type)
    response = requests.get(url, headers = headers)
    text = response.text
    dict_text = json.loads(text)
    print('正在爬取第'+str(page)+'页...')
    if page == 1:
        statuses = dict_text['statuses']
    else:
        statuses = statuses + dict_text['statuses']
    print('当前爬取的数据量:'+str(len(statuses))+'条')
    # 格式化created_time, text
    for index in range(last_index,len(statuses)):
        before_formatting = dict_text['statuses'][index-last_index]['created_at']
        if before_formatting:
            before_formatting = datetime.datetime.fromtimestamp(int(before_formatting) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        dict_text['statuses'][index-last_index]['created_at'] = before_formatting
        temp_text = dict_text['statuses'][index-last_index]['text']
        if temp_text:
            temp_text = re.compile(r'<[^>]+>',re.S).sub('', temp_text)
            print(temp_text)
        dict_text['statuses'][index-last_index]['text'] = temp_text
        if len(dict_text['statuses'][index-last_index]['text']) > 0:
            statuses_formatted.append(dict(发布时间=dict_text['statuses'][index-last_index]['created_at'],转发数=dict_text['statuses'][index-last_index]['retweet_count'],评论数=dict_text['statuses'][index-last_index]['reply_count'],收藏数=dict_text['statuses'][index-last_index]['fav_count'],点赞数=dict_text['statuses'][index-last_index]['like_count'],动态内容=dict_text['statuses'][index-last_index]['text']))
    last_index = len(statuses)
    # 防止反爬虫机制，每爬取100条休息15秒
    if page%100 == 99:
        time.sleep(15)
    # with open(str(userName)+'.csv', 'w', encoding='utf-8', newline='') as fp:
    #     writer = csv.DictWriter(fp,csv_headers)
    #     writer.writeheader()
    #    # writer.writerows(statuses)
    with open(str(userName)+'_Formatted.csv', 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp,csv_headers_statuses_formatted)
        writer.writeheader()
        writer.writerows(statuses_formatted)
