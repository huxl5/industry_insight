#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/4 10:16
# @Author : huxiaoliang
# @Description :
# @See：
# todo:文章日期输出；org提取badcase优化

import csv
import re
import time
from datetime import datetime
import warnings
from urllib.error import HTTPError

from hanlp_restful import HanLPClient

from api_demo.api_demo.utils import file_util
from api_demo.api_demo.utils.mylogger import Logger
from tqdm import tqdm

# 关闭警告
warnings.filterwarnings("ignore")

# hanlpV2.1X api引入
# 创建客户端，填入服务器地址和秘钥：
url = 'https://www.hanlp.com/api'
HanLP = HanLPClient(url, auth='MjMzNkBiYnMuaGFubHAuY29tOjVPaGpUeUI2VkJBVzR6Vmo=', language='zh')

# 日志文件及级别控制


# 获取当前时间
now = datetime.now()
# 格式化时间字符串，作为文件夹名
log_name = now.strftime("%Y%m%d-%H-%M-%S")
log = Logger('../log/{}.log'.format(log_name), level='info')  # warning info


def is_org(val):
    if val[1] == 'ORGANIZATION':
        return True
    else:
        return False


# 所有关键词及对应匹配的正则表达式dict
# (.*)->(.{0,10})-> .{0,10}指定字符个数
keyword_pattrens = {
    '流动性困难': r'流动性.{0,10}(困难|告急|不足|压力|不足|问题|困境|危机)',
    '资金链断裂': r'资金.{0,10}(断裂|困难|告急|不足|压力|不足|问题|困境|危机)',
    '供应链中断': r'供应.{0,30}(中断|生变|限制|风险|重创|问题|紧张|无法.{0,5}恢复)',  # 多数为宏观政策、行业、国际；标题中未识别出实体

    '担保违约': r'担保违约',
    '债务风险': r'债务风险|违约',
    '债务违约': r'债务违约|风险',
    '抽贷': r'抽贷',
    '贷款被清查': r'贷款被清查',
    '断贷': r'断贷',
    '停止提供贷款': r'停止提供贷款',
    '委托贷款逾期': r'贷款逾期',
    '债务清理': r'债务清理',
    '遭做空': r'遭做空|被空头盯上',
    '冻结查封': r'冻结查封',
    '税务黑名单': r'(税务|税收)黑名单',
    '财务造假': r'财务造假|财务风险|数字造假',
    '处罚': r'处罚',
    '审计所被处罚': r'审计所.{0,10}被处罚|审计缺陷|审计.{0,5}被罚|审计违规|审计.{0,5}虚假',
    '内幕交易': r'内幕交易',
    '批评警示': r'批评警示|通报批评',

    '欠息': r'欠息|欠薪|欠税',  # 扩展关键词
    # '欠薪': r'欠薪',
    # '欠税': r'欠税',

    '涉黑': r'涉黑',
    '失信被执行人': r'失信被执行人',
    '违规业务': r'违规',
    '违规担保': r'违规担保',
    '违规借贷': r'违规借贷|违规借款|违规转贷|违规贷款|违规放贷|违规融资',
    '违规举债': r'违规举债',
    '违规买卖股份': r'违规买卖股份',
    '违规披露': r'违规披露',
    '机构踩雷': r'踩雷',
    # '弹劾领导人': r'弹劾领导人', # 政治性事件
    # '美伊局势': r'美伊局势',# 政治性事件
    '被公诉': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}被公诉',
    '被控制': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}被控制',
    '实控人出逃': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}出逃',
    '实控人涉嫌犯罪': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}涉嫌犯罪',
    '实控人失联': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}失联',
    '实际控制人失去控制权': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}失去.{0,10}控制权',
    '实控人破产': r'(CEO|董事长|总经理|实控人|实际控制人|).{0,5}破产',
    '实控人死亡': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}死亡',
    '实控人自杀': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}自杀',
    '实控人违法': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}(违法|违规)',
    '实控人严重违纪': r'(CEO|董事长|总经理|实控人|实际控制人).{0,5}违纪',#必须跟主语一起，否则政治性太强
    # 常务副总
    '实控人':r'实控人.{0,10}(调查|自首|监狱|涉嫌|犯罪|操纵股市|被抓|行贿|被拘|犯罪|强制|刑事|拘留|捕|查|罪|挪用资金|刑拘|内幕交易|操控股价|被调查|操纵|失联|惹祸|批捕|抓获|诈骗|抓捕|归案|欺诈|留置|立案|禁入|非法|跑路|失踪|僵局|)',   # 控制权变更
    '实际控制人失去控制权': r'控制权变更|(CEO|董事长|总经理|实控人|实际控制人).{0,5}失去.{0,10}控制权',
'实控人破产': r'(CEO|董事长|总经理|实控人|实际控制人|).{0,5}破产|注销',

}
# 调试所用，当前关键词
current_keyword = '处罚'
# 数据源列表：todo
sources = [
    'baijiahao',
    'xueqiu',
]

# 资讯文件列表
bjh_news = [
    # 'bjh_res_new_all',
    # 'bjh_res_20230515',
    # 'bjh_res_20230516',
    # 'bjh_res_20230517',
    # 'bjh_res_20230518',
    # 'bjh_res_20230519',
    # 'bjh_res_20230520',
    # 'bjh_res_20230521',
    # 'bjh_res_20230522',
    # 'bjh_res_20230523',
    # 'bjh_res_new1_1',
    # 'bjh_res_all',
    # 'badcase',
    'bjh_res_new_diff',
    # 'bjh_res_new1',
    # 'bjh_res_new2',
    # 'bjh_res_new3',
    # 'bjh_res_new4',
    # 'bjh_res_new',
    # 'bjh_res_new_test',
    # 'bjh_res_new_unit_test1',
]

org_black_pattern = r'国务院|省委|市委|县委|银保监会|证监会|监管局|证监局|审计厅|执行局|法院|交易所|深交所|沪交所|上交所|港交所|信托|证券|财联社|新闻|媒体|财经|日报|时报|观察报|财报|经济网|协会|事务所|联储|董事会|网站$|网$'
org_black_list = ['多米诺骨牌', '专网', '*', '结婚产业观察', '关联', '中国网', '本部']

start_time = time.time()
# 用于存放全量数据及某关键词的数据量
match_cnt = 0
match_org_cnt = 0
cnt = 0
pos_neg_cnt = {0: 0, 1: 0, 2: 0}
dic_match_cnt = {}
dic_match_org_cnt = {}
dic_cnt = {}
dic_pos_neg_cnt = {}
# for bjh_new in tqdm(bjh_news, position=0, desc="处理文件进行中", leave=False, colour='green', ncols=80):
for bjh_new in bjh_news:
    log.logger.info("正在处理文件{}中数据...".format(bjh_new))
    # 结果输出信息
    field_names = ['title',
                   'event_type',
                   'is_match',
                   'unique_orgs',
                   'analysis',
                   'url',
                   'source',
                   'publish_time',
                   'news_time',
                   'title_sentiment_analysis',
                   'abstract_sentiment_analysis',
                   'title_orgs',
                   'abstract_orgs',
                   'abstract',
                   ]
    writer = file_util.get_dictwriter(r'D:\work_softs\workspace-py-citic\industry_insight\data\ner_reslut\baijiahao',
                                      field_names, bjh_new)
    with open(r'D:\work_softs\workspace-py-citic\industry_insight\data\spider_result\baijiahao\{}.csv'.format(bjh_new),
              'r',
              newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='`')
        for row in reader:
            try:
                # 判断关键词
                keyword = row['事件类型']
                if dic_cnt.get(keyword):
                    dic_cnt[keyword] += 1
                else:
                    dic_cnt[keyword] = 1
                cnt += 1

                if "404 Not Found" in row['标题']:
                    log.logger.warn('该详情页爬取失败，{}:{} '.format(row['标题'], row['链接']))
                    continue
                if not keyword:
                    log.logger.warn('{}: 该关键词不存在，请检查检查通过`分列是否有问题 {}:{}'.format(keyword, row['标题'], row['链接']))
                    continue
                pattern = keyword_pattrens.get(keyword)
                if not pattern:
                    log.logger.warn(
                        '{}: 该关键词不存在或其对应正则表达式不存在，请检查keyword_pattrens，或检查通过`分列是否有问题 {}:{}'.format(keyword, row['标题'],
                                                                                                 row['链接']))
                    continue
                # filter rule:fixme 国际or国内；宏光政策、行业or企业 目前提供的关键词字典即为企业资讯，暂时不作处理
                row['数据源'] = 'baijiahao'
                source = row['数据源']
                log.logger.info('正在处理：{}-{}-{}-{}'.format(source, keyword, row['标题'], row['链接']))

                # 逐个关键词输出查看匹配规则
                # if current_keyword ==keyword:
                #     print(row['标题'], row['新闻来源'], row['发布时间'], row['链接'], '\n 摘要：', row['摘要'])
                # # else:
                # #     continue
                # continue

                # filter rule1:关键词命中标题or摘要
                title_match_obj = re.search(pattern, row['标题'])
                abstract_match_obj = re.search(pattern, row['摘要'])
                if title_match_obj or abstract_match_obj:
                    # 计数
                    match_cnt += 1
                    if dic_match_cnt.get(keyword):
                        dic_match_cnt[keyword] += 1
                    else:
                        dic_match_cnt[keyword] = 1
                    # 事件资讯情感分析
                    try:
                        title_sentiment_analysis = round(HanLP.sentiment_analysis(row['标题']), 2)
                        # time.sleep(1.5)
                        abstract_sentiment_analysis = round(HanLP.sentiment_analysis(row['摘要']), 2)
                        # time.sleep(1.5)
                    except HTTPError as err:
                        if err.code == 429:
                            log.logger.error(err.msg)
                            # print("发生请求过多异常了")
                            time.sleep(100)
                            title_sentiment_analysis = round(HanLP.sentiment_analysis(row['标题']), 2)
                            time.sleep(1.5)
                            abstract_sentiment_analysis = round(HanLP.sentiment_analysis(row['摘要']), 2)
                            time.sleep(1.5)
                        else:
                            raise
                    # 正负面：同负；一正一负和小于0；一正一负和大于0；同正
                    tag = ''
                    if title_sentiment_analysis < 0 and abstract_sentiment_analysis < 0:
                        pos_neg_cnt[0] += 1
                        if dic_pos_neg_cnt.get(keyword + '-0'):
                            dic_pos_neg_cnt[keyword + '-0'] += 1
                        else:
                            dic_pos_neg_cnt[keyword + '-0'] = 1
                        tag = "双负"
                    elif title_sentiment_analysis > 0 and abstract_sentiment_analysis > 0:
                        pos_neg_cnt[2] += 1
                        if dic_pos_neg_cnt.get(keyword + '-2'):
                            dic_pos_neg_cnt[keyword + '-2'] += 1
                        else:
                            dic_pos_neg_cnt[keyword + '-2'] = 1
                        tag = "双正"
                    else:
                        pos_neg_cnt[1] += 1
                        if dic_pos_neg_cnt.get(keyword + '-1'):
                            dic_pos_neg_cnt[keyword + '-1'] += 1
                        else:
                            dic_pos_neg_cnt[keyword + '-1'] = 1
                        tag = "一正一负"
                    dic_pos_neg_cnt[keyword + '-最终匹配量'] = (dic_pos_neg_cnt.get(keyword + '-0') if dic_pos_neg_cnt.get(
                        keyword + '-0') else 0) + (dic_pos_neg_cnt.get(keyword + '-1') if dic_pos_neg_cnt.get(
                        keyword + '-1') else 0)
                    # 标题和摘要同时识别为正，则不进行进一步处理
                    if tag == "双正":
                        continue
                    # ner rule：# 对标题、摘要 识别组织机构:只识别标题也可，因为重要新闻往往会重复
                    try:
                        title_ress = HanLP(row['标题'], tasks='ner/msra')['ner/msra']  # ress：按句子切分，三维数组
                        # time.sleep(1.5)
                        abstract_ress = HanLP(row['摘要'], tasks='ner/msra')['ner/msra']
                        # time.sleep(1.5)
                    except HTTPError as err:
                        if err.code == 429:
                            log.logger.error(err.msg)
                            # print("发生请求过多异常了")
                            time.sleep(60)
                            title_ress = HanLP(row['标题'], tasks='ner/msra')['ner/msra']  # ress：按句子切分，三维数组
                            time.sleep(1.5)
                            abstract_ress = HanLP(row['摘要'], tasks='ner/msra')['ner/msra']
                            time.sleep(1.5)
                        else:
                            raise
                    unique_orgs = set()
                    title_orgs = []
                    abstract_orgs = []
                    for res in title_ress:
                        rts = list(filter(is_org, res))
                        if rts:
                            title_orgs.append(rts)
                            for rt in rts:
                                # 对黑名单org进行过滤
                                if rt and rt[0] not in org_black_list and not re.search(org_black_pattern, rt[0]):
                                    unique_orgs.add(rt[0])
                    log.logger.info(
                        "基本信息：{} {} {} {} {} {}".format(row['标题'], title_sentiment_analysis,
                                                        abstract_sentiment_analysis,
                                                        row['新闻来源'], row['发布时间'], row['链接']))
                    # ner rule：fixme：如果标题中已经匹配到title，则暂时不识别摘要数据
                    # if len(unique_orgs)>0:
                    #     continue

                    log.logger.info("abstract:{}".format(row['摘要']))
                    log.logger.info('title_orgs: {}'.format(title_orgs))
                    for res in abstract_ress:
                        rts = list(filter(is_org, res))
                        if rts:
                            abstract_orgs.append(rts)
                            for rt in rts:
                                if rt and rt[0] not in org_black_list and not re.search(org_black_pattern, rt[0]):
                                    unique_orgs.add(rt[0])
                    log.logger.info('abstract_orgs:{}'.format(abstract_orgs))
                    log.logger.info('unique_orgs: {}'.format(unique_orgs))

                    # 将最终结果输出到对应文件
                    # 实体提取结果处理：
                    if len(title_orgs) > 0 or len(abstract_orgs) > 0:
                        match_org_cnt += 1
                        if dic_match_org_cnt.get(keyword):
                            dic_match_org_cnt[keyword] += 1
                        else:
                            dic_match_org_cnt[keyword] = 1
                        # 对提取结果进行过滤
                    dic = {
                        'title': row['标题'],
                        'event_type': row['事件类型'],
                        'is_match': len(unique_orgs) > 0 and tag in ['双负', '一正一负'],
                        'unique_orgs': unique_orgs,
                        'analysis': tag,
                        'url': row['链接'],
                        'source': row['新闻来源'],
                        'publish_time': row['发布时间'],
                        'news_time': row['文章日期'],
                        'title_sentiment_analysis': title_sentiment_analysis,
                        'abstract_sentiment_analysis': abstract_sentiment_analysis,
                        'title_orgs': title_orgs,
                        'abstract_orgs': abstract_orgs,
                        'abstract': row['摘要'],
                    }
                    log.logger.info('情感分类:{}'.format(tag))
                    # 满足条件的输出
                    print("dic:{}".format(dic))
                    writer.writerow(dic)
                    log.logger.info("dic:{}".format(dic))
                    log.logger.info('=' * 300)
            except Exception as e:
                log.logger.error('{}-{}-{}-{}-{}'.format(e, source, keyword, row['标题'], row['链接']))
    log.logger.info("文件{}中数据处理完毕".format(bjh_new))

    # 匹配数量输出；标题/摘要实体提取输出；三个为负向数量输出；人工核对数量食输出
    print(
        '处理完毕，总量：{}，最终匹配量：{}，事件关键词匹配量：{}，可提取org量：{}，均为负：{}，一正一负：{}，均为正：{}'.format(cnt, pos_neg_cnt[0] + pos_neg_cnt[1],
                                                                                  match_cnt,
                                                                                  match_org_cnt, pos_neg_cnt[0],
                                                                                  pos_neg_cnt[1], pos_neg_cnt[2]))
    log.logger.info(
        '处理完毕，总量：{}，最终匹配量：{}，事件关键词匹配量：{}，可提取org量：{}，均为负：{}，一正一负：{}，均为正：{}'.format(cnt, pos_neg_cnt[0] + pos_neg_cnt[1],
                                                                                  match_cnt,
                                                                                  match_org_cnt, pos_neg_cnt[0],
                                                                                  pos_neg_cnt[1], pos_neg_cnt[2]))
    print('处理完毕，总量：{}，总耗时：{:.2f} min，事件关键词匹配量：{}，可提取org量：{}，均为负/一正一负/均为正：{}'.format(dic_cnt, (
            time.time() - start_time) / 60, dic_match_cnt,
                                                                                    dic_match_org_cnt, dic_pos_neg_cnt))
    log.logger.info('处理完毕，总量：{},总耗时：{:.2f} min，事件关键词匹配量：{}，可提取org量：{}，均为负/一正一负/均为正：{}'.format(dic_cnt, (
            time.time() - start_time) / 60, dic_match_cnt,
                                                                                              dic_match_org_cnt,
                                                                                              dic_pos_neg_cnt))

# 数据清洗：
    # 观察结果，修正规则；
    # 四个关键词，50*4；结果统计；观察新规则
    # 目前代码不适合雪球号
    # 不唯一的公司实体
    # eg-通过距离/黑名单解决：基本信息：重庆信托:因债务人流动性困难,昆明融创城集合资金计划实质违约
    # eg-通过黑名单解决：unique_orgs: {'半年', '搜于特集团股份有限公司', '深圳证券交易所'}
    # eg-优先标题中的实体/黑名单/高频重复（标题，正文）:基本信息：隆鑫系两A股公司扣非连续三年下降 涂建华累计逾期债务近150亿财务...
    # 黑名单之一：资讯来源，交易所，信托机构，确认不是org得badcase
    # 可能需要匹配不同得ner识别得api
    # black_list = [
    #     '教育']  # 重庆信托 澎湃新闻 财联社 深圳证券交易所 银保监会  华夏时报 浙江证监局 网易财经 美国半导体行业协会 纽约联储 多米诺骨牌 专网 陕西监管局 国务院 XX证券 '证券日报' '立信会计师事务所'
    # badcase = ['结婚产业观察', '关联']  # 陕西县委  交易所 董事会 深交所 中国证监会 V观财报 * '财经', '中国网'
    # 类型判断：中文，数字，字母
    # 选择长的：{'st中利', 'st', '中利'}
    # 实体重复
    # eg:unique_orgs: {'东旭光电', '东旭光电董事会'}
    # 跟事件名的先后关系：

    # TODO：NER提取公司组织汇总：
    # 1、标题中NER优先；+文字字符距离；+黑名单过滤/badcase过滤
    # 2、文字字符距离；+黑名单过滤/badcase过滤；
    # 匹配规则

    # TODO：时间效率：
    # 只对双负，一正一负得操作

# NER识别+规则
# 记录：雪球
# 雪球网信息比较杂（10之1 2关键词为主要意思）：比如CEO辞职，多数为为国际新闻，多数CEO辞职语义，命中的重复多（自媒体人多）
# 董事长辞职 命中的多为董事长，语义不合
# 流动性困难 国际新闻巨多

# 规则：
# 命中标题（高优），摘要（次优），全文（低优）严格命中，命中分开的关键词 同语义关键词
# 国内新闻or国际新闻判断：eg：来源？
# 目标：国内新闻，中小企业，语义匹配

# 百度百家号
# 标题中完全命中的并不在最前面，是按焦点排序的；调整为按时间排序会好一点，同时按时间排序容易做增量，
# 选择按时间排序，按焦点的话不好做增量，同时，非语义匹配的，因为焦点高而排在前


# 分析百家号：流动性**处理结果
# 标题中基本均包含公司实体名，未识别出来的基本是政策或行业资讯。有部分丢失，也能因为重复新闻得到补充。
# 建议规则：标题和摘要识别关键字过滤数据，公司主体从标题中识别

# 爬虫 TODO：将资讯时间计算一下
