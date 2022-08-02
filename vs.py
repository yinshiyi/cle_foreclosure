# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:21:39 2022

@author: Shiyi Yin
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

report='XS/S\nUnavailable in Runaway Teal\nXS/S'
test=report
while (test==report):
    test=''
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path="C:/Users/Shiyi Yin/Downloads/chromedriver.exe", chrome_options=chrome_options)
    
    driver.get("https://www.victoriassecret.com/us/vs/sleepwear-and-lingerie-catalog/5000000311?genericId=11193810&choice=18M2&size1=XS/S")
    sleep(10)
    driver.find_element("xpath","/html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[1]/div[3]/div[2]/div[1]/div/picture/img").click()
    hover=driver.find_element("xpath","/html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[2]/div[2]/div[1]")
    function=ActionChains(driver).move_to_element(hover)
    function.perform()
    toolTipElement = driver.find_element("xpath","/html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[2]/div[2]/div[1]")
    toolTipText = toolTipElement.text
    test=toolTipText
    print(toolTipText)
    print(time.asctime(time.localtime(time.time())))
    driver.close()
    myFile = open(file="C:/Users/Shiyi Yin/Downloads/log.txt", mode="a")
    print(toolTipText, file=myFile)
    print(time.asctime(time.localtime(time.time())), file=myFile)
    print(' /n',file=myFile)
    myFile.close()
    sleep(300)
# /html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[1]/div[3]/div[2]/div[4]/div/picture/img
# /html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[1]/div[3]/div[2]/div[1]/div/picture/img
# /html/body/div[2]/main/div[1]/div[4]/div/div[4]/div[2]/div[2]/div[1]