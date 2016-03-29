#!/usr/bin/env python2
# coding:utf8

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MoneyData(Base):
    __tablename__ = 'money_data'

    data_id = sa.Column(sa.Integer, primary_key = True, 
            autoincrement = True)

    public_date = sa.Column(sa.Date)
    country_id = sa.Column(sa.ForeignKey('country.country_id'), 
            default =1)

    m0 = sa.Column(sa.Float)
    m1 = sa.Column(sa.Float)
    m2 = sa.Column(sa.Float)


class Country(Base):
    __tablename__ = 'country'

    country_id = sa.Column(sa.Integer, primary_key = True,
            autoincrement = True)

    country_name = sa.Column(sa.String(32), nullable=False)
    country_name_eng = sa.Column(sa.String(32))
    
    money_data = relationship("MoneyData", backref = 'country')


class HolidayType(Base):
    '''假日类别'''
    __tablename__ = 'holiday_type'
    type_id = sa.Column(sa.Integer, primary_key=True)
    type_name = sa.Column(sa.String(16))

    holidays = relationship("Holidays", backref = 'holiday_type')

class Holidays(Base):
    '''假日'''
    __tablename__ = 'holidays'
    holiday_date = sa.Column(sa.Date, primary_key=True)
    holiday_type_id = sa.Column(sa.ForeignKey('holiday_type.type_id'))


class Instrument(Base):
    '''期指数据'''
    __tablename__ = 'instrument'
    data_id = sa.Column(sa.Integer, primary_key=True,
            autoincrement=True)
    instrument_id = sa.Column(sa.String(8), nullable=False)  # 期指的代码
    trading_day = sa.Column(sa.Date, nullable=False)

    open_price = sa.Column(sa.Float)
    highest_price = sa.Column(sa.Float)
    lowest_price = sa.Column(sa.Float)
    close_price = sa.Column(sa.Float)
    
    interest = sa.Column(sa.Float) # 持仓
    presettlement_price = sa.Column(sa.Float)
    settlement_price = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    turnover = sa.Column(sa.Float)

    __table_args__ = (
            sa.UniqueConstraint('instrument_id', 'trading_day'),
            )


class Financing(Base):
    '''融资数据'''
    __tablename__ = 'rongzi'

    data_id = sa.Column(sa.Integer, primary_key=True,
            autoincrement=True)
    trading_day = sa.Column(sa.Date)
    market = sa.Column(sa.String(4))

    financing_remain = sa.Column(sa.Float)
    financing_buy = sa.Column(sa.Float)
    
    stock_remain = sa.Column(sa.Float)
    stock_remain_money = sa.Column(sa.Float)
    stock_sell = sa.Column(sa.Float)
    __table_args__ = (
            sa.UniqueConstraint('trading_day', 'market'),
            )


class FinancingDetail(Base):
    '''融资融券明细'''
    __tablename__ = 'financing_detail'
    
    data_id = sa.Column(sa.Integer, primary_key=True,
            autoincrement=True)
    trading_day = sa.Column(sa.Date)
    market = sa.Column(sa.String(4))
    stock_code = sa.Column(sa.ForeignKey('stock.stock_code'))
    
    financing_remain = sa.Column(sa.Float)
    financing_buy = sa.Column(sa.Float)
    financing_payback = sa.Column(sa.Float)

    stock_remain = sa.Column(sa.Float)
    stock_sell = sa.Column(sa.Float)
    stock_payback = sa.Column(sa.Float)
    stock_remain_money = sa.Column(sa.Float)

    __table_args__ = (sa.UniqueConstraint('stock_code','trading_day'),)



class Stock(Base):
    __tablename__ = 'stock'
    stock_code = sa.Column(sa.String(12), primary_key=True)
    stock_name = sa.Column(sa.String(32))

    financing_details = relationship('FinancingDetail', backref='stock')

class StockNew(Base):
    __tablename__ = 'stock_new'
    stock_code = sa.Column(sa.String(12), primary_key=True)
    stock_name = sa.Column(sa.String(32), nullable=False)
    market = sa.Column(sa.String(8))

class StockAccount(Base):
    __tablename__ = 'stock_account'
    trading_date = sa.Column(sa.Date, unique=True, primary_key=True)

    personal_new = sa.Column(sa.Float)
    company_new = sa.Column(sa.Float)

    personal_total_a = sa.Column(sa.Float)
    personal_total_b = sa.Column(sa.Float)

    company_total_a = sa.Column(sa.Float)
    company_total_b = sa.Column(sa.Float)
    
    position_a = sa.Column(sa.Float)
    position_b = sa.Column(sa.Float)

    trading_a = sa.Column(sa.Float)
    trading_b = sa.Column(sa.Float)


if __name__ == '__main__':
    import os
    from sqlalchemy.orm import sessionmaker

    url = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
    engine = sa.create_engine(url)
    Session = sessionmaker()
    session = Session(bind=engine)

#    Base.metadata.create_all(bind=engine)


