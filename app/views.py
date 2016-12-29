# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from app import app, db

import matplotlib
matplotlib.use('svg')
from matplotlib import pyplot as plt
import StringIO
import numpy as np
import lxml.etree as ET

from .forms import GridParamForm, FundStockForm
from tools import get_grid_price
import re
from dataModels import *

from sqlalchemy import desc
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'nickname': 'Miguel'}
    x=np.linspace(0, 4*np.pi, 200)
    y=np.sin(x)
    plt.plot(x,y)
    plt.xlabel(u'x')
    
    f=StringIO.StringIO()
    plt.savefig(f, format='svg')

    doc = ET.fromstring(f.getvalue())
    svg = ET.tostring(doc).decode('utf-8')
    return render_template("index.html", title='Home', user=user,
            svg=svg)

@app.route('/grid', methods=['GET', 'POST'])
def grid():
     form = GridParamForm()
     price = None
     if form.validate_on_submit():
        price, ratio = get_grid_price(form.start_price.data, 
                form.end_price.data, form.grid_count.data)
     return render_template("grid.html", title='Home',
                form=form, price=price)

@app.route('/fund_stock', methods=['GET', 'POST'])
def fund_stock():
    form = FundStockForm()
    message = ''
    valid = False
    data = []
    basic_url='http://fund.eastmoney.com/'
    if form.validate_on_submit():
        if re.match('\d{6}',form.stock_code.data):
            stock_code = form.stock_code.data
            data = db.session.query(FundStockData).filter(
                FundStockData.stock_code==stock_code).order_by(desc(
                        FundStockData.stock_value_ratio)).all()       
        else:
            stock_name = form.stock_code.data
            stock = db.session.query(StockNew).filter(StockNew.stock_name==stock_name).scalar()
            if stock:
                data = db.session.query(FundStockData).filter(
                    FundStockData.stock==stock).order_by(desc(
                    FundStockData.stock_value_ratio)).all()       

        
    return render_template('fund_stock.html', title=u'基金持仓查询',
            form=form, data=data, basic_url=basic_url)
