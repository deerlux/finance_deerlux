import requests
from dateutil import parser
import json, logging

import dataModels
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO,
                    filename='crawlHsggt.log')

Session = sessionmaker()
engine = sa.create_engine('sqlite:///hsg.db')
session = Session(bind=engine)

url='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTZJZS&token=70f12f2f4f091e459a279469fe49eca5&filter=(DateTime%3E^2014-02-27^)'
response = requests.get(url)
data = json.loads(response.content)

i = 0

for v in data:
    currDate = parser.parse(v['DateTime'])
    if session.query(dataModels.HSGMoney).filter(dataModels.HSGMoney.date==currDate.date()).count() != 0:
        logging.info("data exists skipping: %s" % v['DateTime'])
        continue
    item = dataModels.HSGMoney(
        date = parser.parse(v['DateTime']),
        hs_money = v['HSMoney'] if type(v['HSMoney']) is float else None,
        ss_money = v['SSMoney'] if type(v['SSMoney']) is float else None,
        north_money = v['NorthMoney'] if isinstance(v['NorthMoney'], float) else None,
        gg_hs_money = v['GGHSMoney'] if isinstance(v['GGHSMoney'], float) else None,
        gg_ss_money = v['GGSSMoney'] if isinstance(v['GGSSMoney'], float) else None,
        south_money = v['SouthSumMoney'] if isinstance(v['SouthSumMoney'], float) else None)
    
    session.add(item)
    i += 1
try:
    session.commit()
    logging.info("%d data crawled." %  i)
except ValueError as e:
    print(v['DateTime'])
    session.close()

session.close()


