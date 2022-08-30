from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

ac = os.environ.get("WET_AC")
pw = os.environ.get("WET_PW")

try:
    driver = webdriver.Chrome()
    driver.get('https://wetransfer.com')

    loginButt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navigation.login"]')))
    loginButt.click()

    acInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, '1-email')))
    acInput.send_keys(ac)

    pwInput = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    pwInput.send_keys(pw)
    pwInput.send_keys(Keys.RETURN)

    print('Login Success!')

    cookieButt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/button[1]')))
    cookieButt.click()
    # cookieButt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/button[1]')))
    # cookieButt.send_keys(Keys.RETURN)

    # agreeButt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[2]/button')))
    # agreeButt.click()
    # composeButt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div')))
    # composeButt.click()

except:
    print('Login Failed!')
