# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 13:07:12 2019

@author: Shiyi
"""
import os
os. chdir('C:/Users/Shiyi/Onedrive/python/')
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import html
url = 'https://www.bovada.lv/sports/politics'
options = webdriver.ChromeOptions()
options.add_argument('headless')
#driver = webdriver.PhantomJS('C:/Users/Shiyi/Onedrive/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe',chrome_options=options)
driver.get(url)
time.sleep(2)
#soup=BeautifulSoup(driver.page_source, 'lxml')
summary=driver.find_elements_by_partial_link_text('Politics')
text=[]
for y in range(len(summary)):
    text.append(summary[y].text)                     
print(text)    


url2 = 'https://www.bovada.lv/sports/esports/starcraft'
driver.get(url2)
time.sleep(2)
summary=driver.find_elements_by_partial_link_text('-')
text=[]
for y in range(len(summary)):
    text.append(summary[y].text)                     
print(text) 
