# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 14:06:57 2020

@author: Shiyi
"""
import os
import time
os. chdir('C:/Users/Shiyi/Onedrive/python/')
import csv
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.pullapart.com/inventory/search/?Locations=25,24,11&MakeID=47&Models=1373&LocationID=11")
        
for i in range(1,60):
    sy=driver.find_elements_by_xpath("//*[contains(text(), 'Details')]")
    for elements in sy:
        if elements.text=='DETAILS':
            #wait for the element to be clickable
            elements.click()
            time.sleep(2)
            break

        
sy=driver.find_elements_by_xpath("//*[contains(text(), 'Convertible')]")
for elements in sy:
    print(elements.text)
name=[]
for i in range(1,60):
    ii=driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div/div/div[4]/div[6]/div/div[3]/div[1]/div["+str(i)+"]/div[1]/div[2]/div[2]/div[1]/p")
    if len(ii) >0:
       name.append(ii[0].text) 
