#coding:utf-8
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')
assert u'中文标签云' in browser.title
