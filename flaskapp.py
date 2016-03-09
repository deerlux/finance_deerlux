from flask import Flask

import lxml.etree as ET
import sqlalchemy

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello world</h1>'


if __name__ == '__main__':
    app.run()

