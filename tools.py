import numpy as np
import os
from dataModels import StockNew, Stock 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_grid_price(bottom, top, number):
    ratio = np.power(np.e,(np.log(top) - np.log(bottom))/number)
    return bottom*(ratio**np.arange(number)), ratio


def modify_stock_code():
    engine = create_engine(os.environ['OPENSHIFT_POSTGRESQL_DB_URL'])
    Session = sessionmaker()
    session = Session(bind=engine)

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
        
    from dataModels import *

    pat = re.compile('(.+)\((\d{6})\)')
    
    shs = [pat.findall(x) for x in stocks_raw if pat.findall(x)]
    
    engine = create_engine(os.environ['OPENSHIFT_POSTGRESQL_DB_URL'])
    Session = sessionmaker()
    session = Session(bind=engine)

    for xx in shs:
        try:
            stock = StockNew(stock_code=xx[0][1], stock_name=xx[0][0], 
                    market=market)
            session.add(stock)
        except IndexError:
            print('Error:', xx)

    session.commit()
    
    
