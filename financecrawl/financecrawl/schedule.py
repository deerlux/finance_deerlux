from datetime import date
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataModels import Financing, Holidays

import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


engine = create_engine(os.environ['OPENSHIFT_POSTGRESQL_DB_URL'])
Session = sessionmaker()
session = Session(bind=engine)

#process = CrawlerProcess(get_project_settings())

start_date = date(2012,1,1)
end_date = date(2012,12,31)

curr_date = start_date
holidays = [x.holiday_date for x in session.query(Holidays).all()]

while curr_date<=end_date:  
    temp = session.query(Financing).filter(Financing.trading_day==curr_date).all()
    if temp:
        pass
    elif curr_date.weekday() ==5 or curr_date.weekday() == 6:
        pass
    elif curr_date in holidays:
        pass
    else:  
        print(curr_date)
        os.system('scrapy crawl shrongzi -a date_in=' + curr_date.strftime('%Y%m%d'))
        os.system('scrapy crawl szrongzi -a date_in=' + curr_date.strftime('%Y%m%d'))
#        process.crawl('shrongzi', date_in=curr_date.strftime('%Y%m%d'))

    curr_date = curr_date + timedelta(1)

#process.start()

