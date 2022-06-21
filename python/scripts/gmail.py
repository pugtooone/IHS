from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass

ac = 'zeric.chan@iheartstudios.com'
passWord = getpass('Enter Your Password: ')

try:
    driver = webdriver.Chrome()
    driver.get('https://mail.google.com/mail/u/0/#inbox')

    acInput = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
    acInput.send_keys(ac)

    nextButton = driver.find_element(By.XPATH, '//*[@id ="identifierNext"]')
    nextButton.click()

    pwInput = driver.find_element(By.NAME, 'password')
    pwInput.send_keys(passWord)

    nextButton = driver.find_element(By.XPATH, '//*[@id ="passwordNext"]')
    nextButton.click()

    print('Login Success!')
except:
    print('Login Failed!')
