# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 21:51:26 2022

@author: Shiyi Yin
"""

"""
Write a program that takes an email address and string of text on the command line and then, using Selenium,
logs into your email account and sends an email of the string to the provided address. 
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path="C:/Users/Shiyi Yin/Downloads/chromedriver.exe")
browser.get('http://www.gmail.com')

emailElem = browser.find_element('id','identifierId')
emailElem.send_keys('shiyi.yin.test@gmail.com')
#emailElem.submit()
emailElem.send_keys(Keys.RETURN) 
#sendElem.send_keys(Keys.CONTROL + Keys.RETURN)

time.sleep(2)

passwordElem = browser.find_element('name','password')
passwordElem.send_keys('aianluchen')
passwordElem.send_keys(Keys.RETURN) 


time.sleep(20)

composeElem = browser.find_element('xpath','/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div/div') #this only works half of the time
composeElem.click()

time.sleep(5)

toElem = browser.find_element('name',"to")
toElem.send_keys('shiyi.yin@egenesisbio.com')

time.sleep(2)

subjElem = browser.find_element('name',"subjectbox")
subjElem.send_keys('Test with selenium')

time.sleep(2)

bodyElem = browser.find_element(By.CSS_SELECTOR,"div[aria-label='Message Body']") #this is where I get stuck and not sure what to do here
bodyElem.send_keys('A test email with selenium')

time.sleep(2)

bodyElem.send_keys(Keys.CONTROL + Keys.RETURN)

time.sleep(2)
browser.close()
