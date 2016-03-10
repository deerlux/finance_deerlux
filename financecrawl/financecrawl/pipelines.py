# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from financecrawl.items import RongziItem, RongziMingxiItem
from financecrawl.dataModels import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

import os

engine = create_engine(os.environ['OPENSHIFT_POSTGRESQL_DB_URL'])
Session = sessionmaker()
session = Session(bind=engine)

class RongziPipeline(object):
    '''处理融资融券的数据'''
    def process_item(self, item, spider):
        if type(item) == RongziItem:
            db_item = Financing(trading_day=item['trading_day'],
                market=item['market'],
                financing_remain=item['rongzi_yue'],
                financing_buy=item['rongzi_mairu'],
                stock_remain=item['rongquan_yuliang'],
                stock_remain_money=item['rongquan_yuliang_jine'],
                stock_sell=item['rongquan_maichu'])
        
            session.add(db_item)
            try:
                session.commit()
            except:
                logging.warning('record insert failed')
                session.rollback()
        
        if type(item) == RongziMingxiItem:
            stock_item = Stock(stock_code=item['stock_code'],
                    stock_name=item['stock_name'])
            db_item = FinancingDetail(stock=stock_item,
                    trading_day=item['trading_day'],
                    market=item['market'],
                    financing_remain=item['rongzi_yue'],
                    financing_buy=item['rongzi_mairu'],
                    financing_payback=item['rongzi_changhuan'],
                    stock_remain=item['rongquan_yuliang'],
                    stock_sell=item['rongquan_maichu'],
                    stock_payback=item['rongquan_changhuan'],
                    stock_remain_money=item['rongquan_yue'])
            session.add(db_item)
            try:
                session.commit()
            except:
                logging.warning('record mingxi insert failed')
                session.rollback()

        return item

class FinancecrawlPipeline(object):
    def process_item(self, item, spider):
        return item
