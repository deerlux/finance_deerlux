# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from szrongzi.items import RongziItem, RongziMingxiItem
from finance.dataModels import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionaker

import os

engine = create_engine(os.environ('OPENSHIFT_POSTGRESQL_DB_URL'))
Session = sessionmaker()
session = Session(bind=engine)

class RongziPipeline(object):
    '''处理融资融券的数据'''
    def process_item(self, item, spider):
        if type(item) != RongziItem:
            return item


class FinancecrawlPipeline(object):
    def process_item(self, item, spider):
        return item
