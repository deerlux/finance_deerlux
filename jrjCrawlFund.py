#!/usr/bin/env python
# coding: utf-8


import pymongo
from datetime import datetime
import json
import requests
import dateutil.parser
import logging

client = pymongo.MongoClient(host='localhost')
db = client.test

BASE_URL='http://fund.jrj.com.cn/json/netvaluelist/open?openFundType=1&manaCode=0&pageSize=20000&currentPage=1&sortType=6&order=1&obj=netvaluelist&_=1537405868837'
response = requests.get(BASE_URL)


byteContent = response.content[17:]
# 整个response内容加载到一个字典中
dictNetValues = json.loads(byteContent)
# 将日期相关的转换为python日期类型
currentDate = dateutil.parser.parse(str(dictNetValues['date']))
preDate = dateutil.parser.parse(str(dictNetValues['preDate']))
# openFundNetList是一个json的字符串，再将这个字符串转到一个字典中
openFundNetValueList = [json.loads(x) for x in dictNetValues['openFundNetValueList']]
#openFundNetValueList


for k, fund in enumerate(openFundNetValueList):
    # 写入日期相关的内容
    fund['currentDate'] = currentDate
    fund['preDate'] = preDate    
    try:
    # 将净值相关的内容转换面浮点数
        fund['unitNetChngPct'] = float(fund['unitNetChngPct'])
        fund['unitNet'] = float(fund['unitNet'])
        fund['accumNet'] = float(fund['accumNet'])
        fund['unitNetPre'] = float(fund['unitNetPre'])
        fund['accumNetPre'] = float(fund['accumNetPre'])
        fund['unitNetChng'] = float(fund['unitNetChng'])
    except TypeError:
        continue
    # 会自动建库
    db['FundNetValue'].insert_one(fund)
    logging.info("%d records is saved" % k)

