import numpy as np
import os
from dataModels import StockNew, Stock, StockDayPrice 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas_datareader.data as web
from sqlalchemy import or_
import gzip, pickle
import logging
 
engine = create_engine(os.environ['OPENSHIFT_POSTGRESQL_DB_URL'])
Session = sessionmaker()
session = Session(bind=engine)


def get_grid_price(bottom, top, number):
    ratio = np.power(np.e,(np.log(top) - np.log(bottom))/number)
    return bottom*(ratio**np.arange(number)), ratio


def modify_stock_code():
    stocks = session.query(Stock)
    for stock in stocks:
        if stock.stock_code.startswith('5') or stock.stock_code.startswith('6'):
            stock.stock_code += '.SH'
        else:
            stock.stock_code += '.SZ'

    session.commit()


def import_stock(shstock_file='shstock.pkl.gz', market='sh'):
    from cPickle import load
    import gzip
    import re
    
    with gzip.open(shstock_file) as f:
        stocks_raw = load(f)
        
    pat = re.compile('(.+)\((\d{6})\)')
    
    shs = [pat.findall(x) for x in stocks_raw if pat.findall(x)]
    
    for xx in shs:
        try:
            stock = StockNew(stock_code=xx[0][1], stock_name=xx[0][0], 
                    market=market)
            session.add(stock)
        except IndexError:
            print('Error:', xx)

    session.commit()
    
def yahoo_stock_download(stock_code, market, start_date=None, end_date=None):
    logging.basicConfig(level=logging.INFO)

    if market.lower() == 'sh':
        ps = '.ss'
    elif market.lower() == 'sz':
        ps = '.sz'
    else:
        return  

    code = stock_code + ps
    logging.info('Starting crawl the data from yahoo: %s' % code)
    try:
        data = web.DataReader(code, 'yahoo')
    except Exception as e:
        logging.error('Error to crawl %s' % code)
        logging.error(e.message)
        return

    logging.info('Data crawl finished: %s' % code)
    
    with gzip.open(code+'.pkl.gz', 'wb') as f:
        pickle.dump(data, f)
    
    for date in data.index:
        stock_day_price = StockDayPrice(stock_code=stock_code,
                open_price = data.ix[date]['Open'],
                high_price = data.ix[date]['High'],
                low_price = data.ix[date]['Low'],
                close_price = data.ix[date]['Close'],
                volume = data.ix[date]['Volume'],
                adj_close = data.ix[date]['Adj Close'],
                trading_date = date.date())
        session.add(stock_day_price)
        
    try:
        session.commit()
        logging.info('{0} of {1} is inserted'.format(len(data.index), 
            code))
    except Exception as e:
        logging.error('Error occured: %s' % e.message)
        session.rollback()

if __name__ == '__main__':

    stocks = session.query(StockNew).filter(
            or_(StockNew.stock_code.like('0%'),
            StockNew.stock_code.like('3%'), 
            StockNew.stock_code.like('6%'))).all()
    
    for stock in stocks:
        yahoo_stock_download(stock.stock_code, stock.market)

 
