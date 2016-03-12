# -*- coding: utf-8 -*-
import scrapy

import datetime
from financecrawl.items import StockAccountItem

class StockaccountSpider(scrapy.Spider):
    name = "stockaccount"
    allowed_domains = ["www.chinaclear.cn"]
    start_urls = []
    #['http://www.chinaclear.cn/cms-webapp/wcm/getManuscriptByTitle_mzkb.action?weekflag=prevWeek&dateStr=2016.03.07']

    def __init__(self, date_in=None, *args, **kwargs):
        super(StockaccountSpider, self, *args, **kwargs)

        today = datetime.date.today()

        if not date_in:
            crawl_date = datetime.date.today() - datetime.timedelta(today.weekday())
        else:
            crawl_date = date_in - datetime.timedelta(date_in.weekday())

        self.crawl_date = crawl_date

        dateStr = crawl_date.strftime("%Y.%m.%d")
        
        baseurl = 'http://www.chinaclear.cn/cms-webapp/wcm/getManuscriptByTitle_mzkb.action?weekflag=prevWeek&dateStr='
        self.start_urls.append(baseurl+dateStr)


    def parse(self, response):
        if response.status != 200:
            return
        try:
            texts = response.xpath('//tbody//td[2]//span/text()').extract()
        except IndexError as e:
            self.logger.info('Error occured when parse result {0}'.format(
                reponse.url))
            return
        
        str2float = lambda x: float(x.replace(',',''))
    
        item = StockAccountItem()
        item['trading_date'] = self.crawl_date
        item['personal_new'] = str2float(texts[2])
        item['company_new'] = str2float(texts[3])
        item['personal_total_a'] = str2float(texts[6])
        item['personal_total_b'] = str2float(texts[7])
        item['company_total_a'] = str2float(texts[9])
        item['company_total_b'] = str2float(texts[10])
        item['position_a'] = str2float(texts[12])
        item['position_b'] = str2float(texts[13])
        item['trading_a'] = str2float(texts[15])
        item['trading_b'] = str2float(texts[16])
        
        return item
