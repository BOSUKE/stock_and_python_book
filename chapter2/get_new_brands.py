# -*- coding: utf-8 -*-
import datetime
import sqlite3

from pyquery import PyQuery
from tqdm import tqdm


def new_brands_generator():
    url = 'http://www.jpx.co.jp/listing/stocks/new/index.html'
    q = PyQuery(url)
    for d, i in tqdm(zip(q.find('tbody > tr:even > td:eq(0)'),
                    q.find('tbody > tr:even span')), desc="新上場銘柄をパースし、DBにinsert..."):
        date = datetime.datetime.strptime(d.text, '%Y/%m/%d').date()
        yield (i.get('id'), date)

def insert_new_brands_to_db(db_file_name):
  conn = sqlite3.connect(db_file_name)
  with conn:
    sql = 'INSERT INTO new_brands(code,date) VALUES(?,?)'
    conn.executemany(sql, new_brands_generator())
