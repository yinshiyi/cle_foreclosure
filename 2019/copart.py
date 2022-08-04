# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 13:13:13 2019

@author: Shiyi
"""

copartid='COPART015C'
#192B casper wy 
#atlanta-west-ga-015C/
#A&B
#054C NC - RALEIGH
#159 flint wed
#061 detroit tues
#161 Kincheloe wed
#160 ionia friday
#103 lansing friday
#880C Eastern region Thursday
#https://www.freelancer.com/projects/php/copart-iaai-scraper/
import os
os. chdir('C:/Users/Shiyi/Onedrive/python/')
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# when did a certain vehicle sold?
# how much does a certain vehicle with lot number sell for?
# how much does multiple vehicle sell for?
url = 'https://g2auction.copart.com/g2/#/'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe')
#driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe',chrome_options=options)
driver.get(url)
#//*[@id="serverSideDataTable"]/tbody/tr/td[9]/span
#//*[@id="serverSideDataTable"]/tbody/tr[2]/td[9]/span
#//*[@id="serverSideDataTable_info"]
#python_button = driver.find_element_by_id("COPART034A")
time.sleep(5)
python_button=WebDriverWait(driver, 1000000000).until(
        EC.visibility_of_element_located((By.ID, copartid))
        )
#python_button = driver.find_element_by_id(copartid)
python_button.click()
print('program initialization success, logging started')
time.sleep(3)

tempprice=[0]
finalprice=[]
lotnum=[]

for y in range(100000):
    time.sleep(0.1)
    newbid=driver.find_elements_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor')
    if len(newbid)>0:
        temp=newbid[0].text
        if temp[0] == '$' :
            price= int((temp.split("\n")[0]).replace(',', '').replace('$',''))
            if price != tempprice[-1]:
                tempprice.append(price)
        if temp[0] == 'S' and len(tempprice)>1:
            finalprice.append(tempprice[-1])
            lotnum.append(driver.find_element_by_xpath('//*[@id="lotDesc-'+copartid+'"]/div[1]/div[2]/a').text)
            tempprice=[0]
    else:
        break
df=pd.DataFrame()
df['lotnum']=lotnum
df['price']=finalprice 
df.to_csv('copart'+time.strftime("%Y%m%d-%H%M%S")+'.csv')


