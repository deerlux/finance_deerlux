# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import scrapy
import datetime, os, re
import xlrd
from financecrawl.items import RongziItem, RongziMingxiItem
from dateutil import parser
from financecrawl.dataModels import get_max_trading_date, Financing, get_previous_trading_date, get_next_trading_date
from financecrawl.settings import DB_URL, LOG_LEVEL
import logging

from scrapy.shell import inspect_response

#def is_weekend(in_date):
#    '''判断是否是周末
#    in_date     是一个日期类型的变量
#    返回值：    如果是周末则返回假否则返回真'''
#    weekday = in_date.weekday()
#    if weekday == 5 or weekday == 6:
#        return True
#    else:
#        return False

is_weekend = lambda x: x.weekday() ==5 or x.weekday()==6
gen_url = lambda crawl_date: '{0}{1}{2}{3}'.format(
       'http://www.sse.com.cn/market/dealingdata/overview/margin/a/',
       'rzrqjygk',
       crawl_date.strftime('%Y%m%d'),
       '.xls')

class ShrongziSpider(scrapy.Spider):
    name = "shrongzi"
    allowed_domains = ["www.sse.com.cn"]
    start_urls = []

    def __init__(self, date_in=None, *args, **kwargs):
        super(ShrongziSpider, self).__init__(*args, **kwargs)
        if date_in:
            crawl_date = parser.parse(date_in)
            self.start_urls.append(gen_url(crawl_date))
        else:
            max_date = get_max_trading_date(metadata=Financing,
                    url=DB_URL,
                    market='sh')
            self.logger.debug('max date is {0}'.format(max_date))

            if max_date is None:
                start_date = get_previous_trading_date(datetime.date.today())
            else:
                start_date = get_next_trading_date(max_date)

            end_date = get_previous_trading_date(datetime.date.today())
            crawl_date = start_date
            while crawl_date <= end_date:
                self.start_urls.append(gen_url(crawl_date))
                crawl_date = get_next_trading_date(crawl_date)         

    def parse(self, response):
        if response.status != 200:
            self.logger.debug('Error to crawl page from %s' % response.url)
            return 

        self.logger.info("Crawled url: {0}".format(response.url))
        
        try:
            xls = xlrd.open_workbook(file_contents=response.body)
        except Exception as e:
            self.logger.error(e)
            yield None

        sheet1 = xls.sheet_by_index(0)
        sheet2 = xls.sheet_by_index(1)
        
        datestr = re.findall('\d+', os.path.basename(response.url))[0]
        trading_day = datetime.datetime.strptime(datestr, "%Y%m%d")
        
# 首先处理汇总数据，是第一个sheet，这个sheet只有两行，第一行是标题，第二行是数据
        if sheet1.nrows < 2:
            self.logger.error("The sheet of summary data'row less than 2")
            yield 

        k = 1
        item = RongziItem()
        item["trading_day"] = trading_day
        item["market"] = "sh"
        item["rongzi_yue"] = float(sheet1.row_values(k)[0])
        item["rongzi_mairu"] = float(sheet1.row_values(k)[1])
        item["rongquan_yuliang"] = float(sheet1.row_values(k)[2])
        item["rongquan_yuliang_jine"] = float(sheet1.row_values(k)[3])
        item["rongquan_maichu"] = float(sheet1.row_values(k)[4])
        yield item
        
# 然后处理明细数据，第二个sheet
        mingxi_item = RongziMingxiItem()
        mingxi_item["trading_day"] = trading_day
        mingxi_item['market']='sh'

        index = range(1,sheet2.nrows)
        mingxi_item['stock_code'] = [sheet2.row_values(x)[0] for x in index]
        mingxi_item['stock_name'] = [sheet2.row_values(x)[1] for x in index]

        mingxi_item["rongzi_yue"] = [float(sheet2.row_values(k)[2]) for k in index]
        mingxi_item["rongzi_mairu"] = [float(sheet2.row_values(k)[3]) for k in index] 
        mingxi_item["rongzi_changhuan"] = [float(sheet2.row_values(k)[4]) for k in index]
        mingxi_item["rongquan_yuliang"] = [float(sheet2.row_values(k)[5]) for k in index]
        mingxi_item["rongquan_maichu"] = [float(sheet2.row_values(k)[6]) for k in index]
        mingxi_item["rongquan_changhuan"] = [float(sheet2.row_values(k)[7]) for k in index]

        mingxi_item["rongquan_yue"] = [None for k in index]
        
        yield mingxi_item
 
