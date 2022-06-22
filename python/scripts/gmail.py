#! python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyinputplus as pyin
import time

ac = 'zeric.chan@iheartstudios.com'
pw = pyin.inputPassword('Enter Your Password: ')

try:
    driver = webdriver.Chrome()
    driver.get('https://mail.google.com/mail/u/0/#inbox')

    acInput = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
    acInput.send_keys(ac)
    acInput.send_keys(Keys.RETURN)

    time.sleep(1)

    pwInput = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    pwInput.send_keys(pw)
    pwInput.send_keys(Keys.RETURN)

    print('Login Success!')

    time.sleep(1)

    composeButt = driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div')
    composeButt.click()

    time.sleep(1)

    emailSubInput = driver.find_element(By.XPATH, '//*[@id=":q3"]')
    emailSubInput.send_keys('job')
except:
    print('Login Failed!')
