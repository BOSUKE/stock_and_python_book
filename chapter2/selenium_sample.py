# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('http://jp.kabumap.com/servlets/kabumap/Action?SRC=basic/top/base&codetext=7203')
unit = driver.find_element_by_css_selector('#minUnit').text
print(unit)
