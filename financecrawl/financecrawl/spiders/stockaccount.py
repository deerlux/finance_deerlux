# -*- coding: utf-8 -*-
import scrapy

import datetime
from financecrawl.items import StockAccountItem
from dateutil.parser import parse

class StockaccountSpider(scrapy.Spider):
    name = "stockaccount"
    allowed_domains = ["www.chinaclear.cn"]
    start_urls = []

    def __init__(self, date_in=None, *args, **kwargs):
        super(StockaccountSpider, self, *args, **kwargs)

        today = datetime.date.today()

        if not date_in:
            crawl_date = datetime.date.today() - datetime.timedelta(today.weekday()+3) 
        else:
            temp_date = parse(date_in).date()
            crawl_date = temp_date - datetime.timedelta(temp_date.weekday())

        self.crawl_date = crawl_date

        self.dateStr = crawl_date.strftime("%Y.%m.%d")
        
        self.baseurl = 'http://www.chinaclear.cn/cms-search/view.action?action=china'
        
    def start_requests(self):
        return [scrapy.FormRequest(self.baseurl, formdata={'channelIdStr':'6ac54ce22db4474abc234d6edbe53ae7', 'dateStr':self.dateStr})]

    def parse(self, response):
        if response.status != 200:
            return
       
        result = response.xpath('//td//tbody//tr')
        if len(result) <21:
            self.logger.error('Error occured when parse result {0}'.format(
                response.url))
            return
        rel_xpath = './/td[2]//span/text()'

        str2float = lambda x: float(x.strip().replace(',',''))

        extract_data = lambda x: str2float(result[x].xpath(rel_xpath).extract()[0])
    
        item = StockAccountItem()
        item['trading_date'] = self.crawl_date

        item['personal_new'] = extract_data(2)
        item['company_new'] = extract_data(3)

        item['personal_total_a'] = extract_data(7)
        item['personal_total_b'] = extract_data(8)
        item['company_total_a'] = extract_data(11)
        item['company_total_b'] = extract_data(12)
        item['position_a'] = extract_data(15)
        item['position_b'] = extract_data(16)
        item['trading_a'] = extract_data(19)
        item['trading_b'] = extract_data(20)

        self.logger.info('The following url is parsed: {0}'.format(response.url))
        
        return item
