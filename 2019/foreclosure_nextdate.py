# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:24:33 2019

@author: Shiyi
"""
#https://www.google.com/maps/dir/2476+Derbyshire+Rd,+Cleveland+Heights,+OH+44106,+USA/9530+Cove+Drive,+North+Royalton,+OH/
#//*[@id="section-directions-trip-0"]/div[2]/div[1]/div[1]/div[1]/span[1]
#https://www.geeksforgeeks.org/python-calculate-distance-duration-two-places-using-google-distance-matrix-api/
import os
os.chdir('C:/Users/Shiyi/Onedrive/python/')
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
#this block of code is to scrape the data
url = 'https://cpdocket.cp.cuyahogacounty.us/SheriffSearch/search.aspx'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe',chrome_options=options)
#ie diriver
#driver = webdriver.PhantomJS('C:/Users/Shiyi/Onedrive/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.implicitly_wait(4)
driver.get(url)
driver.find_element_by_id("SheetContentPlaceHolder_c_search1_btnNonTax").click()

#get the distance to homebase by drivering time on google map
#can use driver to insert selected link here
time.sleep(1)
addresslist=[]
statuslist=[]
pricelist=[]
orginalpricelist=[]
date=[]
totalpage=driver.find_element_by_xpath('//*[@id="SheetContentPlaceHolder_C_searchresults_lblPage"]')
num=int(totalpage.text[2:6])
for y in range(num):
    #driver.findElements(By.XPATH('//*[@id="SheetContentPlaceHolder_C_searchresults_btnNext"]')).size() != 0
#    python_button = driver.find_element_by_xpath('//*[@id="SheetContentPlaceHolder_C_searchresults_btnNext"]')
#    python_button.click()
#    time.sleep(5)
    time.sleep(5)
    for x in range(15):
        url1="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblAddress_"
        url2='"]'
        #address= WebDriverWait(driver, 10).until(
        #        EC.presence_of_element_located((By.XPATH, url1+str(x)+url2))
        #)
        #address= WebDriverWait(driver, 10).until(
        #        EC.visibility_of_element_located((By.XPATH, url1+str(x)+url2))
        #)
        url3='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblStatus_'
        url4='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblOpeningBid_'
        url5='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblAppraised_'
        url7='//*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lblResidentialText_'
        address=driver.find_elements_by_id(url1+str(x))
        #the element is not found becasue the page has less than 15 elements
        if len(address) > 0:
            addresslist.append(address[0].text+" cuyahoga county, OH")
        # //*[@id="SheetContentPlaceHolder_C_searchresults_gvSaleSummary_lnkCaseNum_xx"] contain CV
            status=driver.find_element_by_xpath(url3+str(x)+url2)
            statuslist.append(status.text)
        #price=WebDriverWait(driver, 10).until(
        #        EC.visibility_of_element_located((By.XPATH, url4+str(x)+url2))
        #)
            price=driver.find_element_by_xpath(url4+str(x)+url2)
            pricelist.append(float(price.text.replace(',', '').replace('$','')))
        #orginalprice=WebDriverWait(driver, 10).until(
        #        EC.visibility_of_element_located((By.XPATH, url5+str(x)+url2))
        #)
            orginalprice=driver.find_element_by_xpath(url5+str(x)+url2)
            orginalpricelist.append(float(orginalprice.text.replace(',', '').replace('$','')))
            if driver.find_element_by_xpath(url7+str(x)+url2):
                date.append(driver.find_element_by_xpath(url7+str(x)+url2).text[-10:])
            else:
                date.append('')
    print('lol')
    if y < (num-1): 
        element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "SheetContentPlaceHolder_C_searchresults_btnNext"))
                )
        element.send_keys(webdriver.common.keys.Keys.SPACE)
        print('really')
    else:
        print()
#ignore error of no such elements
#IF NOT SOLD ON 08/12/2019 IT WILL BE RE-OFFERED ON 08/26/2019, these opening bid is 0
# this block of code summarize everything
addresslist.append('2476 Derbyshire Rd')
statuslist.append('ACTIVE')
pricelist.append(10000)
orginalpricelist.append(10000)
date.append('')
df = pd.DataFrame(addresslist,columns=['Address'])
df['status']=statuslist
df['price']=pricelist
df['orignialprice']=orginalpricelist
#set the auction date to majority
df['date']=[max(set(date), key = date.count) if x is '' else x for x in date]
#if the last auction happening correct for the mininum bid to zero
df.loc[df['date'] != max(set(date), key = date.count),'price']=0
dftotal=df
df= df.loc[(df['orignialprice'] > 0) &(df['status']=='ACTIVE')& (df['price']< 50000)]
df.sort_values("Address", inplace = True) 
df.drop_duplicates(subset ="Address", keep = 'first', inplace = True) 
# this block of code is to transform the address to gps location
gps = []
latitude =[]
longitude=[]
zipcode=[]
income=[]
asian=[]
white=[]
for index, row in df.iterrows():
    temp=geolocator.geocode(row['Address'])
    gps.append(temp)
    time.sleep(1)
    if temp:
        latitude.append(float(temp.latitude))
        longitude.append(float(temp.longitude))
        zipcode.append(int(temp.address.split(",")[-2]))
        urlincome1='http://www.justicemap.org/index.php?gsLayer=income_block&gfLon='
        urlincome2='&gfLat='
        urlincome3='&giZoom=15&gsGeo=block&giAdvanced=1&'
        driver.get(urlincome1+str(temp.longitude)+urlincome2+str(temp.latitude)+urlincome3)
        time.sleep(1)
        income.append(str(driver.find_element_by_xpath('//*[@id="fulldemotable"]/table/tbody/tr/td[2]').text))
        if driver.find_element_by_xpath('//*[@id="fulldemotable"]/table/tbody/tr[4]/td[2]').text:
            asian.append(float(driver.find_element_by_xpath('//*[@id="fulldemotable"]/table/tbody/tr[4]/td[2]').text[:-1]))
        else:
            asian.append(0)
        if driver.find_element_by_xpath('//*[@id="fulldemotable"]/table/tbody/tr[10]/td[2]').text:
            white.append(float(driver.find_element_by_xpath('//*[@id="fulldemotable"]/table/tbody/tr[10]/td[2]').text[:-1]))
        else:
            white.append(0)
    else:
        latitude.append(41.502176)
        longitude.append(-81.591807)
        zipcode.append(44106)
        income.append(40000)
        asian.append(20)
        white.append(80)
df['gps'] = gps
df['latitude']=latitude
df['longitude']=longitude 
df['zipcode']=zipcode 
df['white']=white
df['asian']=asian
df['income']=income
# https://www.latlong.net/
# http://maps.huge.info/zip.htm
# scrap http://www.justicemap.org/index.php?gsLayer=&gfLon=-81.51080787&gfLat=41.45228757
#http://www.justicemap.org/data.php
#http://www.justicemap.org/index.php?gsLayer=income_block&gfLon=-81.591807&gfLat=41.502176&giZoom=15&gsGeo=block&giAdvanced=1&
#income //*[@id="fulldemotable"]/table/tbody/tr[1]/td[2]
#asian //*[@id="fulldemotable"]/table/tbody/tr[4]/td[2]
#white //*[@id="fulldemotable"]/table/tbody/tr[10]/td[2]
# this block of code is to compare gps location to the safezone area

polygon = Polygon([(41.498948, -81.606302), (41.508461, -81.601455), (41.520737, -81.555853), (41.481087, -81.565041)])
safelist=[]
for index, row in df.iterrows():
    point= Point(row['latitude'],row['longitude'])
    safelist.append(polygon.contains(point))
df['safe']=safelist

df_out=df.loc[(df['longitude'] > -81) |(df['longitude']<-82.5)]
df_in=df.loc[~df['zipcode'].isin([44112,44103,44104,44105,44102,44109,44110,44117,44119,44123,44128,44137,44146,44132])]
# this block of code filter out the non-active cases and non-safe
df_safe=df[safelist]



# this block of code write the final dataframe to csv.writer
#f = open("forclosure.txt", "w")
#f.write(str(list))
#f.close()
df_in.to_csv('nextdate.csv')

#df = pd.read_csv("foreclosure.csv") 

# this block of code is to plot the map

import subprocess
subprocess.check_call(["C:/Program Files/R/R-3.5.2/bin/Rscript.exe" ,"rassit.R"], shell=False)

os.remove('nextdate.csv')
