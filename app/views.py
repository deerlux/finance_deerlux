# -*- coding: utf-8 -*-
from flask import render_template
from app import app

import matplotlib
matplotlib.use('svg')
from matplotlib import pyplot as plt
import StringIO
import numpy as np
import lxml.etree as ET


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    x=np.linspace(0, 4*np.pi, 200)
    y=np.sin(x)
    plt.plot(x,y)
    plt.xlabel(u'x座标')
    
    f=StringIO.StringIO()
    plt.savefig(f, format='svg')

    doc = ET.fromstring(f.getvalue())
    svg = ET.tostring(doc).decode('utf-8')

    return render_template("index.html", title='Home', user=user,
            svg=svg)

