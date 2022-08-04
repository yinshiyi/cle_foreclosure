# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:26:17 2019

@author: Shiyi
"""

from selenium import webdriver
import time
import sys
#this script will download moives from yesmoive, you need webdriver chrom, input the url
#run examples as following: yesmovie.py "https://yesmovies.ai/film/kevin-hart-what-now/watching.html?ep=0"
url=sys.argv[1]
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/Shiyi/Onedrive/python/chromedriver.exe',options=options)
driver.get(url)
time.sleep(6)
a=driver.find_element_by_xpath('//*[@id="media-player"]/iframe')
url=a.get_attribute('src')
newurl=url.replace("streaming.php", "download")
driver.get(newurl)
b=driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[4]/div[3]/a')
driver.get(b.get_attribute('href'))
