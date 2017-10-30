# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from bs4 import BeautifulSoup
from collections import namedtuple
import sys
import requests

from .parser import parse_krysha
from .parser import combine_url
from .parser import parse_fst_page
from .get_form import get_form

app = Flask(__name__, static_url_path='')


# @app.route('/dist/<path:path>')
# def send_css(path):
#     return send_from_directory('templates/flat-ui-master/dist', path)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def receive_form():
    gf = get_form()
    url = combine_url(**gf)
    pf, max_page=parse_krysha(url)
    # for flat in pf:
    #     prs=flat.price
    # print (from_agency*300)
    # result = parse_krysha(price_from, price_to)
    for p in pf:
    	print(p.price)
    return url+ ' ' +str(len(pf))+ ' ' +str(max_page)
