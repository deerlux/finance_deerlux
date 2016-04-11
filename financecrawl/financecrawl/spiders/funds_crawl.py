# -*- coding: utf-8 -*-
import scrapy
from financecrawl.items import FundItem, FundStockItem
import os, re
from dateutil.parser import parse
from financecrawl.settings import DB_URL
from financecrawl.dataModels import Fund

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL)
Session = sessionmaker()
session = Session(bind=engine)

class FundsCrawlSpider(scrapy.Spider):
    name = "funds_crawl"
    allowed_domains = ["fund.eastmoney.com"]
    start_urls = (
        'http://fund.eastmoney.com/fund.html',
    )

    def __init__(self, crawl='value', *args, **kwargs):
        '''crawl: 可取值'basic', 'position', 'value',确定抓取哪些信息
        basic抓取基金代码、名称、类型、公司、持仓等，
        value抓取净值
        position抓取持仓，如果抓取净值和持仓必须先抓取完basic'''
        super(FundsCrawlSpider, self).__init__(*args, **kwargs)
        self.crawl = crawl.split(',')

    def parse(self, response):
        if 'basic' in self.crawl: 
            try:
                temp = response.xpath('//span[@class="nv"][1]/text()').extract()[0]
                total_page_parsed = True
            except Exception as e:
                self.logger.error(e)
                self.logger.error('Error to parse total pages string from start urls')
                total_page_parsed = False
    
            if total_page_parsed: 
                try:
                    total_pages = int(re.findall('\d+', temp)[0])
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error('Error to parse total pages from {0}'.format(temp))
                base_url = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={0},200&dt=1460126012690&atfc=&onlySale=0'
        
                for page in range(1, total_pages+1):
                    url = base_url.format(page)
                    yield scrapy.Request(url, self.parse_page)

        if 'position' in self.crawl:
            funds = session.query(Fund).all()
            for fund in funds:
                url = 'http://fund.eastmoney.com/{0}.html'.format(fund.fund_code)
                yield scrapy.Request(url, self.parse_position)
            
    def parse_page(self, response):
        temp = re.sub(r'([\{,])([a-z]+)(:)', r'\1"\2"\3', response.body)
        exec(temp.strip('var '))

        for i in db['datas']:
            fund_code = i[0]
            fund_name = i[1]
            if 'basic' in self.crawl.strip().split(','):
                # 抓取基金的基本信息
                url = 'http://fund.eastmoney.com/{0}.html'.format(fund_code)
                yield scrapy.Request(url, self.parse_basic)
            else:
                pass
            if 'value' in self.crawl.strip().split(','):
                pass
    
    def parse_basic(self, response):
        item = FundItem()
        temp = ''.join(response.xpath('//div[@class="infoOfFund"]/table//tr[1]/td[1]//text()').extract())
        fund_type = temp.split(u'：')[1]
        fund_code = re.findall(r'\d+', response.url)[0]
        fund_name = response.xpath('//div[@class="fundDetail-tit"]//text()').extract()[0].strip('(')
        fund_company = response.xpath('//div[@class="infoOfFund"]/table//tr[2]/td[2]/a/text()').extract()[0]

        item['fund_code'] = fund_code
        item['fund_name'] = fund_name
        item['fund_type'] = fund_type
        item['fund_company'] = fund_company
        return item
    
    def parse_position(self, response):
        # 持仓相关内容
        public_date_str = response.xpath('//*[@id="position_shares"]/div[2]/span/text()').extract()[0]
        try:
            public_date = parse(public_date_str.split(':')[1]).date()
            crawl_position = True
        except Exception as e:
            self.logger.warning(e)
            self.logger.warning(public_date_str)
            crawl_position = False

        if crawl_position:
            stocks_url = response.xpath('//div[@id="quotationItem_DataTable"]//li[@class="position_shares"]//table//tr//td[1]//a/@href').extract()
            stocks_name = response.xpath('//*[@id="position_shares"]//tr//td[1]/a/text()').extract()
            ratios_str = response.xpath('//div[@id="quotationItem_DataTable"]//li[@class="position_shares"]//table//tr//td[2]//text()').extract()
            for url, stock_name, ratio in zip(stocks_url, stocks_name, ratios_str):
                item = FundStockItem()
                item['stock_code'] = re.findall(r'\d+', url)[0]
                item['stock_name'] = stock_name
                item['fund_code'] = re.findall(r'\d+',response.url)[0]
                item['stock_value_ratio'] = float(ratio.strip('%'))
                item['public_date'] = public_date
                yield item

                

