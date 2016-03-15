# -*- coding: utf-8 -*-
import scrapy
import datetime, re, string

import lxml
from financecrawl.items import RongziItem, RongziMingxiItem
from dateutil.parser import parse


def str2float(str_in):
    if type(str_in) is list:
        return [string.atof(''.join(x.split(','))) for x in str_in]
    else:
        return string.atof(string.join(str_in.split(','), ''))

class SzrongziSpider(scrapy.Spider):
    name = "szrongzi"
    allowed_domains = ["www.szse.cn"]
    start_urls = ('http://www.szse.cn/main/disclosure/rzrqxx/rzrqjy/',)

    def __init__(self, date_in=None, *args, **kwargs):
        super(SzrongziSpider, self).__init__(*args, **kwargs)
        if date_in:
            self.date_in = parse(date_in).date()
        else:
            self.date_in = None

    def parse(self, response):
        if self.date_in:
            txtDate = self.date_in.strftime('%Y-%m-%d')
        else:
            txtDate = response.xpath('//form[@name="frmtab2"]//tr[1]//span[2]/text()').extract()[0]

        urlbase1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab1&txtDate='
        urlbase2 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2&txtDate='

        yield(scrapy.Request(urlbase1+txtDate, callback=self.parse_excel))
        yield(scrapy.Request(urlbase2+txtDate, callback=self.parse_excel))

#    def __init__(self, category=None, *args, **kwargs):
#        super(SzrongziSpider, self).__init__(*args, **kwargs)
#
#        day = datetime.date.today() - datetime.timedelta(1)
#
#
#        urlbase1 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab1&txtDate='
#        urlbase2 = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2&txtDate='
#        
#        self.start_urls.append(urlbase1 + day.strftime('%Y-%m-%d'))
#        self.start_urls.append(urlbase2 + day.strftime('%Y-%m-%d'))

    def parse_excel(self, response):
        if response.status != 200:
            return

        if response.url.find('TABKEY=tab1') != -1:
            item = RongziItem()

            doc = lxml.html.fromstring(response.body)
            try:
                item['rongzi_mairu'] = str2float(doc.xpath('//tr/td[1]/text()')[1])
                item['rongzi_yue'] = str2float(doc.xpath('//tr/td[2]/text()')[1])
                item['rongquan_maichu'] = str2float(doc.xpath('//tr/td[3]/text()')[1])
                item['rongquan_yuliang'] = str2float(doc.xpath('//tr/td[4]/text()')[1])
                item['rongquan_yuliang_jine'] = str2float(doc.xpath('//tr/td[5]/text()')[1])
            except IndexError, e:
                self.logger.error('{0} : {1}'.format(response.url, e.message))
                return     
        
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
