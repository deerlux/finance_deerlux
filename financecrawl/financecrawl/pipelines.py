# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from financecrawl.items import RongziItem, RongziMingxiItem, StockAccountItem
from financecrawl.dataModels import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

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
            except IntegrityError as e:
                logging.warning('record insert failed: {0}'.format(e.message.decode('utf-8')))
                session.rollback()
        
        if type(item) == RongziMingxiItem:
            if not type(item['stock_code']) is list:
                self.process_single_mingxi_item(item)
            else:
                self.process_multiple_mingxi_item(item)
            
        return item
    
    def process_single_mingxi_item(self, item):
        '''处理只有一支股票数据的情况'''
        stock_item = Stock(stock_code=item['stock_code'],
                stock_name=item['stock_name'])
        
        self.update_stock_table(stock_item)

        db_item = FinancingDetail(stock_code=stock_item.stock_code,
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
        except IntegrityError as e:
            logging.warning('record mingxi insert failed: {0}'.format(e.message.decode('utf-8')))
            session.rollback()

    def update_stock_table(self, stock):
        '''判断股票数据在不在stock表中，如果没有的话插入，如果股票名称更改则改之
        stock为Stock ORM类型'''
        
        result = session.query(Stock).filter(Stock.stock_code==stock.stock_code).all()

        if len(result) == 0:
            session.add(stock)
            session.commit()
            logging.info('stock info is inserted: %s: %s' %(stock.stock_code, stock_name.decode('utf-8'))) 

        elif len(result) == 1:
            if result[0].stock_name != stock.stock_name:
                result[0].stock_name = stock.stock_name
                session.commit()
                logging.info('stock name is updated: %s: %s -> %s' % (stock.stock_code, 
                    result[0].stock_name.decode('utf-8'), stock_name.decode('utf-8')))
       

    def process_multiple_mingxi_item(self, item):
        '''深市的抓取数据每次返回一个数据集统一进行处理'''

        for i, code in enumerate(item['stock_code']):
            stock = Stock(stock_code=code, stock_name=item['stock_name'][i])
            self.update_stock_table(stock)
            
        mingxi_new = []
        for i, code in enumerate(item['stock_code']):
            mingxi_new.append(
                  {'trading_day':item['trading_day'],
                   'market':'sz',
                   'stock_code':code,
                   'rongzi_yue':item['rongzi_yue'][i],
                   'rongzi_mairu':item['rongzi_mairu'][i],
                   'rongquan_yuliang':item['rongquan_yuliang'][i],
                   'rongquan_maichu':item['rongquan_maichu'][i],
                   'rongquan_yue':item['rongquan_yue'][i]})

        conn = engine.connect()
        ins = FinancingDetail.__table__.insert()

        try:
            conn.execute(ins, mingxi_new)
        except IntegrityError as e:
            logging.warning('Error to insert stock rongzi data to database: {0}'.format(e.message.decode('utf-8')))
            
        logging.info('{0} stock rongzi data is inserted to database'.format(len(item['stock_code'])))
        
        return item

class StockAccountPipeline(object):
    def process_item(self, item, spider):
        if not (type(item) is StockAccountItem):
            return item
        
        db_item = StockAccount()
        
        columns = ['trading_date', 'personal_new', 'company_new',
                'personal_total_a', 'company_total_a',
                'personal_total_b', 'company_total_b',
                'position_a', 'position_b',
                'trading_a', 'trading_b']

        for column in columns:
            exec('db_item.{0} = item["{0}"]'.format(column))

        session.add(db_item)
        try:
            session.commit()
        except Exception as e:
            logging.error('Error when insert stockaccount: {0}'.format(e))
            session.rollback()

        return item
