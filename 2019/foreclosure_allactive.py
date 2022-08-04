# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 13:13:49 2019

@author: Shiyi
"""
#%matplotlib inline
import os
os. chdir('C:/Users/Shiyi/Onedrive/python/')
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
geolocator = Nominatim(user_agent="shiyi")
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt
#from selenium.webdriver.chrome.options import Options
#a=Options().add_argument("--headless")
#driver = webdriver.Chrome(chrome_options=a)
#this block of code is to scrape the data
url = 'https://cpdocket.cp.cuyahogacounty.us/SheriffSearch/results.aspx?q=searchType%3ddate_range%26searchString%3d%26foreclosureType%3d%26dateFrom%3d%26dateTo%3dforeclosureType%3d%27TAX%27%2c+%27TAXB%27'
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe')
driver.implicitly_wait(4)
driver.get(url)
addresslist=[]
statuslist=[]
pricelist=[]
orginalpricelist=[]
totalpage=driver.find_element_by_xpath('//*[@id="SheetContentPlaceHolder_C_searchresults_lblPage"]')
for y in range(int(totalpage.text[2:6])-4):
    #driver.findElements(By.XPATH('//*[@id="SheetContentPlaceHolder_C_searchresults_btnNext"]')).size() != 0
#    python_button = driver.find_element_by_xpath('//*[@id="SheetContentPlaceHolder_C_searchresults_btnNext"]')
#    python_button.click()
#    time.sleep(5)
    time.sleep(5)
    for x in range(15):
        url1='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblAddress_'
        url2='"]'
        address= WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, url1+str(x)+url2))
        )
        address= WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, url1+str(x)+url2))
        )
        #driver.find_element_by_xpath(url1+str(x)+url2)
        addresslist.append(address.text+" cuyahoga county, OH")
        # //*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lnkCaseNum_xx"] contain CV
        url3='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblStatus_'
        status=driver.find_element_by_xpath(url3+str(x)+url2)
        statuslist.append(status.text)
        url4='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblOpeningBid_'
        price=WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, url4+str(x)+url2))
        )
        #driver.find_element_by_xpath(url4+str(x)+url2)
        pricelist.append(float(price.text.replace(',', '').replace('$','')))
        url5='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblAppraised_'
        orginalprice=WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, url5+str(x)+url2))
        )
        #driver.find_element_by_xpath(url4+str(x)+url2)
        orginalpricelist.append(float(orginalprice.text.replace(',', '').replace('$','')))
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "SheetContentPlaceHolder_C_searchresults_btnNext"))
    )
    element.send_keys(webdriver.common.keys.Keys.SPACE)
#ignore error of no such elements

# this block of code summarize everything
df = pd.DataFrame(addresslist,columns=['Address'])
df['status']=statuslist
df['price']=pricelist
df['orignialprice']=orginalpricelist
dftotal=df
df= df.loc[(df['orignialprice'] > 0) &(df['status']=='ACTIVE')& (df['price']< 100000)]
df.sort_values("Address", inplace = True) 
df.drop_duplicates(subset ="Address", keep = 'first', inplace = True) 

# this block of code is to transform the address to gps location
gps = []
latitude =[]
longitude=[]
zipcode=[]
for index, row in df.iterrows():
    temp=geolocator.geocode(row['Address'])
    gps.append(temp)
    time.sleep(1)
    if temp:
        latitude.append(float(temp.latitude))
        longitude.append(float(temp.longitude))
        zipcode.append(int(temp.address[-10:-5]))
    else:
        latitude.append(41.502176)
        longitude.append(-81.591807)
        zipcode.append(44106)
df['gps'] = gps
df['latitude']=latitude
df['longitude']=longitude 
df['zipcode']=zipcode 
# https://www.latlong.net/
# http://maps.huge.info/zip.htm
# scrap http://www.justicemap.org/index.php?gsLayer=&gfLon=-81.51080787&gfLat=41.45228757
#http://www.justicemap.org/data.php

# this block of code is to compare gps location to the safezone area

polygon = Polygon([(41.498948, -81.606302), (41.508461, -81.601455), (41.520737, -81.555853), (41.481087, -81.565041)])
safelist=[]
for index, row in df.iterrows():
    point= Point(row['latitude'],row['longitude'])
    safelist.append(polygon.contains(point))
df['safe']=safelist

df_out=df.loc[(df['longitude'] > -81) |(df['longitude']<-82.5)]
df_in=df.loc[~df['zipcode'].isin([44112,44103,44104,44105,44102,44109,44110,44117,44119,44123,44128,44137,44146])]
# this block of code filter out the non-active cases and non-safe
df_safe=df[safelist]



# this block of code write the final dataframe to csv.writer
#f = open("forclosure.txt", "w")
#f.write(str(list))
#f.close()
df.to_csv('foreclosure.csv')
df_in.to_csv('finalist.csv')

#df = pd.read_csv("foreclosure.csv") 

# this block of code is to plot the map
plt.style.use('seaborn-whitegrid')
y= df['latitude']
x = df['longitude']
line, = plt.plot([-81.588013, -81.579906],[41.508590, 41.511611],'ro-', linewidth=2)
plt.plot(x, y, 'o', color='black');
plt.savefig('map_active.png')

plt.style.use('seaborn-whitegrid')
y= df_safe['latitude']
x = df_safe['longitude']
line, = plt.plot([-81.588013, -81.579906],[41.508590, 41.511611],'ro-', linewidth=2)
plt.plot(x, y, 'o', color='black');
plt.savefig('map_safe.png')

plt.style.use('seaborn-whitegrid')
y= df_in['latitude']
x = df_in['longitude']
# plot mayfield and cedar
line, = plt.plot([-81.588013, -81.579906],[41.508590, 41.511611],'ro-', linewidth=2)
plt.plot(x, y, 'o', color='black');
plt.savefig('map_in.png')