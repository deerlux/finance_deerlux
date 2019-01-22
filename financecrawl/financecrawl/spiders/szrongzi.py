# -*- coding: utf-8 -*-
import scrapy
import datetime, re, string

import lxml
from financecrawl.items import RongziItem, RongziMingxiItem
from dateutil.parser import parse
from financecrawl.dataModels import get_max_trading_date, Financing, get_previous_trading_date, get_next_trading_date
from financecrawl.settings import DB_URL

import logging

import datetime

def str2float(str_in):
    if type(str_in) is list:
        return [float(''.join(x.split(','))) for x in str_in]
    else:
        return float(''.join(str_in.split(',')))

class SzrongziSpider(scrapy.Spider):
    name = "szrongzi"
    allowed_domains = ["www.szse.cn"]
    start_urls = ('http://www.szse.cn/main/disclosure/rzrqxx/rzrqjy/',)

    def __init__(self, date_in=None, *args, **kwargs):
        super(SzrongziSpider, self).__init__(*args, **kwargs)
        if date_in:
            try:
                self.date_in = parse(date_in).date()
            except Exception as e:
                logging.error('{0}'.format(e))
                return
        else:
            max_date = get_max_trading_date(metadata=Financing,
                    url=DB_URL,
                    market='sz')
            if max_date is None:
                self.date_in = None
            else:
                self.date_in = []
                end_date = get_previous_trading_date(datetime.date.today())
                crawl_date = get_next_trading_date(max_date)
                while crawl_date<=end_date:
                    self.date_in.append(crawl_date)
                    crawl_date = get_next_trading_date(crawl_date)

    def parse(self, response):
        urlbase1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab1&txtDate='
        urlbase2 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2&txtDate='
        
        if type(self.date_in) is list:
            for crawl_date in self.date_in:
                txtDate = crawl_date.strftime('%Y-%m-%d')
                yield(scrapy.Request(urlbase1+txtDate, callback=self.parse_excel))
                yield(scrapy.Request(urlbase2+txtDate, callback=self.parse_excel))
        elif type(self.date_in) is datetime.date:
            txtDate = self.date_in.strftime('%Y-%m-%d')
            yield(scrapy.Request(urlbase1+txtDate, callback=self.parse_excel))
            yield(scrapy.Request(urlbase2+txtDate, callback=self.parse_excel))
        else:
            txtDate = response.xpath('//form[@name="frmtab2"]//tr[1]//span[2]/text()').extract()[0]
            yield(scrapy.Request(urlbase1+txtDate, callback=self.parse_excel))
            yield(scrapy.Request(urlbase2+txtDate, callback=self.parse_excel))



    def parse_excel(self, response):
        if response.status != 200:
            return

        if response.url.find('TABKEY=tab1') != -1:
            item = RongziItem()

            doc = lxml.html.fromstring(response.body)
# TODO: 这块后续要改为，如果doc.xpath得出的结果长度大于1,则将两个字符串连接起来再进行转换
            try:
                item['rongzi_mairu'] = str2float(doc.xpath('//tr/td[1]/text()')[0])
                item['rongzi_yue'] = str2float(doc.xpath('//tr/td[2]/text()')[0])
                item['rongquan_maichu'] = str2float(doc.xpath('//tr/td[3]/text()')[0])
                item['rongquan_yuliang'] = str2float(doc.xpath('//tr/td[4]/text()')[0])
                item['rongquan_yuliang_jine'] = str2float(doc.xpath('//tr/td[5]/text()')[0])
            except IndexError as e:
                self.logger.error('{0} : {1}'.format(response.url, e.message))
                raise e
                #return     
        
            date_str = re.findall('txtDate=([\d-]+)', response.url)[0]
        
            item['trading_day'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            item['market'] = 'sz'

            return item
        
        if response.url.find('TABKEY=tab2') != -1:
            
            doc = lxml.html.fromstring(response.body)
            
            item = RongziMingxiItem()
            
            item['stock_code'] = doc.xpath('//tr/td[1]/text()')[1:]
            item['stock_name'] = doc.xpath('//tr/td[2]/text()')[1:]
            item['rongzi_mairu'] = str2float(doc.xpath('//tr/td[3]/text()')[1:])
            item['rongzi_yue'] = str2float(doc.xpath('//tr/td[4]/text()')[1:])
            item['rongquan_maichu'] = str2float(doc.xpath('//tr/td[5]/text()')[1:])
            item['rongquan_yuliang'] = str2float(doc.xpath('//tr/td[6]/text()')[1:])
            item['rongquan_yue'] = str2float(doc.xpath('//tr/td[7]/text()')[1:])               
            item['rongquan_changhuan'] = None
            item['rongzi_changhuan'] = None
                    
            item['market'] = 'sz'
            date_str = re.findall('txtDate=([\d-]+)', response.url)[0]        
            item['trading_day'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            
            return item

#
