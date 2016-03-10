# -*- coding: utf-8 -*-
import scrapy
import scrapy.log
import datetime, os, re
import xlrd
from financecrawl.items import RongziItem, RongziMingxiItem

def is_weekend(in_date):
    '''判断是否是周末
    in_date     是一个日期类型的变量
    返回值：    如果是周末则返回假否则返回真'''
    weekday = in_date.weekday()
    if weekday == 5 or weekday == 6:
        return True
    else:
        return False

 
class ShrongziSpider(scrapy.Spider):
    name = "shrongzi"
    allowed_domains = ["www.sse.com.cn"]
    day = datetime.date.today() - datetime.timedelta(1)
    url = '{0}{1}{2}{3}'.format(
            'http://www.sse.com.cn/market/dealingdata/overview/margin/a/',
            'rzrqjygk', 
            day.strftime('%Y%m%d'), 
            '.xls')
    start_urls = (url,)

    def parse(self, response):
        self.log("Crawled url: {0}".format(response.url), scrapy.log.INFO)
        
        xls = xlrd.open_workbook(file_contents=response.body)
        sheet1 = xls.sheet_by_index(0)
        sheet2 = xls.sheet_by_index(1)
        
        datestr = re.findall('\d+', os.path.basename(response.url))[0]
        trading_day = datetime.datetime.strptime(datestr, "%Y%m%d")
            
        for k in range(sheet1.nrows):
            if k == 0:
                continue
            item = RongziItem()
            item["trading_day"] = trading_day
            item["market"] = "sh"
            item["rongzi_yue"] = float(sheet1.row_values(k)[0])
            item["rongzi_mairu"] = float(sheet1.row_values(k)[1])
            item["rongquan_yuliang"] = float(sheet1.row_values(k)[2])
            item["rongquan_yuliang_jine"] = float(sheet1.row_values(k)[3])
            item["rongquan_maichu"] = float(sheet1.row_values(k)[4])
            yield item

        for k in range(sheet2.nrows):
            if k == 0:
                continue
            mingxi_item = RongziMingxiItem()
            
            mingxi_item["trading_day"] = trading_day
            mingxi_item["market"] = "sh"
            try:
                mingxi_item["stock_code"] = sheet2.row_values(k)[0]
                mingxi_item["stock_name"] = sheet2.row_values(k)[1]
                mingxi_item["rongzi_yue"] = float(sheet2.row_values(k)[2])
                mingxi_item["rongzi_mairu"] = float(sheet2.row_values(k)[3])
                mingxi_item["rongzi_changhuan"] = float(sheet2.row_values(k)[4])
                mingxi_item["rongquan_yuliang"] = float(sheet2.row_values(k)[5])
                mingxi_item["rongquan_maichu"] = float(sheet2.row_values(k)[6])
                mingxi_item["rongquan_changhuan"] = float(sheet2.row_values(k)[7])
                mingxi_item["rongquan_yue"] = None
            except Exception as e:
                self.log(e, scrapy.log.ERROR)

            yield mingxi_item
 
