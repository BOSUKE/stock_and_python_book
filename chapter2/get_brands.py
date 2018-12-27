# -*- coding: utf-8 -*-
from pyquery import PyQuery
import time
import sqlite3


def get_brand(code):
  url = 'https://kabutan.jp/stock/?code={}'.format(code)

  q = PyQuery(url)

  if len(q.find('div.company_block')) == 0:
    return None

  try:
    name = q.find('div.company_block > h3').text()
    code_short_name =  q.find('#stockinfo_i1 > div.si_i1_1 > h2').text()
    short_name = code_short_name[code_short_name.find(" ") + 1:]
    market = q.find('span.market').text()
    unit_str = q.find('#kobetsu_left > table:nth-child(4) > tbody > tr:nth-child(6) > td').text()
    unit = int(unit_str.split()[0].replace(',', ''))
    sector = q.find('#stockinfo_i2 > div > a').text()
  except (ValueError, IndexError):
    return None

  return code, name, short_name, market, unit, sector

def brands_generator(code_range):
  for code in code_range:
    brand = get_brand(code)
    if brand:
      yield brand
    time.sleep(1)

def insert_brands_to_db(db_file_name, code_range):
  conn = sqlite3.connect(db_file_name)
  with conn:
    sql = 'INSERT INTO brands(code,name,short_name,market,unit,sector) ' \
          'VALUES(?,?,?,?,?,?)'
    conn.executemany(sql, brands_generator(code_range))
