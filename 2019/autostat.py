# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:41:32 2019

@author: Shiyi
"""

import os
os. chdir('C:/Users/Shiyi/Onedrive/python/')
from selenium import webdriver
import time
import numpy
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# when did a certain vehicle sold?
# how much does a certain vehicle with lot number sell for?
# how much does multiple vehicle sell for?
urldream = 'https://www.copart.com/lotSearchResults/?free=true&query=pontiac%20g6&searchCriteria=%7B%22query%22:%5B%22pontiac%20g6%22%5D,%22filter%22:%7B%22BODY%22:%5B%22body_style:%5C%22CONVERTI%5C%22%22%5D,%22FETI%22:%5B%22lot_features_code:LOTFEATURE_0%22%5D,%22TITL%22:%5B%22title_group_code:TITLEGROUP_C%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:true%7D'
url = 'https://www.copart.com/lotSearchResults/?free=true&query=pontiac%20g6&searchCriteria=%7B%22query%22:%5B%22pontiac%20g6%22%5D,%22filter%22:%7B%22BODY%22:%5B%22body_style:%5C%22CONVERTI%5C%22%22%5D,%22FETI%22:%5B%22lot_features_code:LOTFEATURE_0%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:true%7D'
urlstat='https://autoastat.com/search?field='
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe')
#driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe',chrome_options=options)
driver.get(url)
time.sleep(5)
lotnum=[]

for tr in driver.find_elements_by_xpath('//*[@id="serverSideDataTable"]'):
    tds = tr.find_elements_by_tag_name('td')
old_list=([td.text for td in tds])
new_list = numpy.array(old_list).reshape(-1, 15)
df2=pd.DataFrame(new_list).drop(columns=[1,13,14])
df2[2]=df2[2].str.replace('\nWatch','')




#old= pd.read_excel('pontic_masterlist.xlsx')




#finalprice=[]
for i, row in df2.iterrows():
#i in len(old['Lot #']):
#    if df2[0][i] != df2[0][i]:
    if len(df2[0][i]) == 0:
        #print(i)
        driver.get(urlstat+str(df2[2][i]))
        time.sleep(2)
        if driver.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div[2]/div[1]/h2/span'):
            df2[0][i]=int(driver.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div[2]/div[1]/h2/span')[0].text[1:-4].replace(' ',''))


df2.columns=df2.columns.values.astype('str')
df2['0']=df2['0'].replace('', np.nan)
df2['2']=df2['2'].astype('int')


old = pd.read_csv("pontic.csv").drop(columns=['Unnamed: 0'])
#pd.concat([df3, df2], axis=1,join='inner', sort=True,ignore_index=True)
old.append(df2, ignore_index=True).drop_duplicates(subset=['0','2'],keep= 'last')
old.drop_duplicates(subset=['0'],keep= 'last')
old.to_csv('pontic.csv')

the ones that are not in the old csv




