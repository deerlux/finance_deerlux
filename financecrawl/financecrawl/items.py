# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RongziItem(scrapy.Item):
    '''交易所融资融券统计数据'''
    trading_day = scrapy.Field()
    market = scrapy.Field()
    rongzi_yue = scrapy.Field()
    rongzi_mairu = scrapy.Field()
    rongquan_yuliang = scrapy.Field()
    rongquan_yuliang_jine = scrapy.Field()
    rongquan_maichu = scrapy.Field()
    stock_name = scrapy.Field()


class RongziMingxiItem(scrapy.Item):
    '''单支或多支股票/基金融资融券数据'''
    trading_day = scrapy.Field()
    market = scrapy.Field()
    stock_code = scrapy.Field()
    rongzi_yue = scrapy.Field()
    rongzi_mairu = scrapy.Field()
    rongzi_changhuan = scrapy.Field()
    rongquan_yuliang = scrapy.Field()
    rongquan_maichu = scrapy.Field()
    rongquan_changhuan = scrapy.Field()
    rongquan_yue = scrapy.Field()
    stock_name = scrapy.Field()

class StockAccountItem(scrapy.Item):
    trading_date = scrapy.Field()

    personal_new = scrapy.Field()
    company_new = scrapy.Field()

    personal_total_a = scrapy.Field()
    personal_total_b = scrapy.Field()

    company_total_a = scrapy.Field()
    company_total_b = scrapy.Field()
    
    position_a = scrapy.Field()
    position_b = scrapy.Field()

    trading_a = scrapy.Field()
    trading_b = scrapy.Field()


