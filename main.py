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
import cx_Oracle

from .parser import parse_krysha
from .parser import combine_url
from .parser import parse_fst_page
from .get_form import get_form
from .oracle_queries import open_connection
from .oracle_queries import close_connection
from .oracle_queries import create_table_of_flats
from .oracle_queries import drop_table_flat_info
from .oracle_queries import drop_table_urls
from .oracle_queries import truncate_table
from .oracle_queries import create_table_of_urls
from .oracle_queries import insert_into_flats
from .oracle_queries import insert_into_urls

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
    open_connection()
    drop_table_flat_info()
    drop_table_urls()
    create_table_of_urls()
    create_table_of_flats()
    insert_into_urls(url)
    for f in pf:
        insert_into_flats(f.link, f.city, f.dist,
         f.mcr_dist, f.address, f.floor, f.max_floor, f.room_number, f.square, f.price, 
         f.descr, f.update_date, url)
    # for flat in pf:
    #     prs=flat.price
    # print (from_agency*300)
    # result = parse_krysha(price_from, price_to)
    for p in pf:
    	print(p.price)
    return url+ ' ' +str(len(pf))+ ' ' +str(max_page)
