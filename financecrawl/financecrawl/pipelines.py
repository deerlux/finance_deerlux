# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from financecrawl.items import *
from financecrawl.dataModels import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from financecrawl.settings import DB_URL

import logging

import os

engine = create_engine(DB_URL)
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
                logging.error('record insert failed: {0}'.format(e.message.decode('utf-8')))
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
            logging.error('record mingxi insert failed: {0}'.format(e.message.decode('utf-8')))
            session.rollback()

        return item

    def update_stock_table(self, stock):
        '''判断股票数据在不在stock表中，如果没有的话插入，如果股票名称更改则改之
        stock为Stock ORM类型'''
        
        result = session.query(Stock).filter(Stock.stock_code==stock.stock_code).all()

        if len(result) == 0:
            session.add(stock)
            session.commit()
            logging.info('stock info is inserted: %s: %s' %(stock.stock_code, stock.stock_name.decode('utf-8'))) 

        elif len(result) == 1:
            if result[0].stock_name != stock.stock_name:
                result[0].stock_name = stock.stock_name
                session.commit()
                logging.info('stock name is updated: {0}: {1} -> {2}'.format(stock.stock_code, 
                    result[0].stock_name, stock.stock_name))
       

    def process_multiple_mingxi_item(self, item):
        '''深市的抓取数据每次返回一个数据集统一进行处理'''

        for i, code in enumerate(item['stock_code']):
            stock = Stock(stock_code=code, stock_name=item['stock_name'][i])
            self.update_stock_table(stock)
            
        mingxi_new = []
        for i, code in enumerate(item['stock_code']):
            mingxi_new.append(
                {'trading_day':item['trading_day'],
                    'market':item['market'],
                    'stock_code':code,
                    'financing_remain':item['rongzi_yue'][i],
                    'financing_buy':item['rongzi_mairu'][i],
                    'stock_remain':item['rongquan_yuliang'][i],
                    'stock_sell':item['rongquan_maichu'][i],
                    'stock_remain_money':item['rongquan_yue'][i]})

        conn = engine.connect()
        ins = FinancingDetail.__table__.insert()

        try:
            conn.execute(ins, mingxi_new)
            logging.info('{0} records is inserted'.format(len(item['stock_code'])))
        except IntegrityError as e:
            logging.error('Error to insert stock rongzi data to database: {0}'.format(e.message.decode('utf-8')))
        
        return item

class StockAccountPipeline(object):
    '''处理股票账户新开户数据'''
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
            logging.error('Error when insert stockaccount: {0}'.format(e.message.decode('utf-8')))
            session.rollback()

        return item

class FundBasicPipeline(object):
    '''处理基金基础信息的类'''
    def process_item(self, item, spider):
        if not (type(item) is FundItem):
            return item

        def safe_get_company_id(item):
            company = item['fund_company']
            cid = session.query(FundCompany.company_id).filter(FundCompany.company_name==company).scalar()
            if cid:
                return cid
            db_com = FundCompany(company_name=company)
            session.add(db_com)
            try:
                session.commit()
                logging.info('Fund company {0} is inserted.'.format(company))
                return db_com.company_id
            except Exception as e:
                logging.error(e)
                session.rollback()
                raise

        def safe_get_type_id(item):
            type_name = item['fund_type']
            tid = session.query(FundType.type_id).filter(FundType.type_name==type_name).scalar()
            if tid:
                return tid

            db_type = FundType(type_name=type_name)
            session.add(db_type)
            try:
                session.commit()
                logging.info('Fund type {0} is inserted.'.format(type_name))
                return db_type.type_id
            except Exception as e:
                logging.error(e)
                session.rollback()
                raise

        fund_code = item['fund_code']
        try:
            session.query(Fund).filter(Fund.fund_code==fund_code).one()
            return 
        except Exception:
            db_fund = Fund(fund_code=fund_code,
                    fund_name = item['fund_name'],
                    type_id = safe_get_type_id(item),
                    company_id = safe_get_company_id(item))
            session.add(db_fund)
            try:
                session.commit()
                logging.info('{0}: {1} is inserted.'.format(fund_code,item['fund_name']))
            except Exception as e:
                logging.error(e)
                session.rollback()
                raise

        
class FundStockPipeline(object):
    '''处理基金的股票持仓数据'''
    def process_item(self, item, spider):
        if not type(item) is FundStockItem:
            return item
        db_item =FundStockData()
        db_item.fund_code = item['fund_code']
        #db_item.stock_code = item['stock_code']
        db_item.public_date = item['public_date']
        db_item.stock_value_ratio = item['stock_value_ratio']

        stock_code = item['stock_code']
        stock_name = item['stock_name']

        stock = session.query(StockNew).filter(StockNew.stock_code==stock_code).scalar()
        if not stock:            
            if stock_code.startswith('0') or stock_code.startswith('3') or stock_code.startswith('1'):
                market = 'sz';
            else:
                market = 'sh';
            stock = StockNew(stock_code=stock_code,
                    stock_name=stock_name,
                    market=market,
                    available=True)
            
        db_item.stock=stock
        session.add(db_item)
        try:
            session.commit()
            logging.info('{0} {1} for fund {2} is inserted: {3}'.format(db_item.stock_code, 
                db_item.stock_value_ratio,
                db_item.fund_code,
                db_item.public_date))
        except Exception as e:
            logging.error(u'{0}'.format(e.message.decode('utf-8')))
            session.rollback()
            
