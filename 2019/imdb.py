# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:28:36 2019

@author: Shiyi
"""

import csv
from selenium import webdriver
driver = webdriver.Firefox()
driver.get("http://example.com/")
table = driver.find_element_by_css_selector("#tableid")
with open('eggs.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    for row in table.find_elements_by_css_selector('tr'):
        wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])