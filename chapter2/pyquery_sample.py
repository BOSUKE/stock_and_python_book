# -*- coding: utf-8 -*-
from pyquery import PyQuery

q = PyQuery('https://kabutan.jp/stock/?code=7203')
sector = q.find('#stockinfo_i2 > div > a')[0].text
print(sector)
