import pandas_datareader.data as web
import gzip, pickle
import os.path
import logging

logging.basicConfig(level=logging.INFO, filename='crawl_yahoo.log',
        format='[%(levelname)s]: %(asctime)s %(filename)s:%(lineno)d %(message)s')


def crawl_yahoo():
    with open('stocks.txt') as f:
        stocks = f.readlines()
    
    stocks = [stock.strip() for stock in stocks]
    
    for stock in stocks:
        if stock.startswith('6'):
            ps = '.ss'
        elif stock.startswith('0') or stock.startswith('3'):
            ps = '.sz'
        else:
            logging.info('Skipping %s' % stock)
            continue

        code = stock + ps
        filename = code + '.pkl.gz'

        if os.path.exists(filename):
            logging.info('%s exists, skipping...' % filename) 
            continue

        try:
            data = web.DataReader(code, 'yahoo')
        except Exception as e:
            logging.warn(e)
            logging.warn('Error when crawl %s' % code)
            continue

        with gzip.open(filename, 'wb') as f:
            pickle.dump(data, f)
        logging.info("%s is finished!" % code)

if __name__ == '__main__':
    crawl_yahoo()
