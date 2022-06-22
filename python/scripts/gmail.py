#! python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyinputplus as pyin
# import time

ac = 'zeric.chan@iheartstudios.com'
pw = pyin.inputPassword('Enter Your Password: ')

try:
    driver = webdriver.Chrome()
    driver.get('https://mail.google.com/mail/u/0/#inbox')

    acInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id ="identifierId"]')))
    acInput.send_keys(ac)
    acInput.send_keys(Keys.RETURN)

    pwInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    pwInput.send_keys(pw)
    pwInput.send_keys(Keys.RETURN)

    print('Login Success!')

    composeButt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div')))
    composeButt.click()


    """emailSubInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id=":q3"]')))
    emailSubInput.send_keys('job')

    emailMsgInput =WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id=":r9"]')))
    emailMsgInput.send_keys('Hi,\nMessage Here\n')"""

except:
    print('Login Failed!')
