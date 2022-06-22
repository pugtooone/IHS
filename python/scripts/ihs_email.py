#! python3
# copy email template to the clipboard

# version:
# 2.0.0: autofill gmail new message

# plan: 
# 1) paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

import sys, os, time
from pathlib import Path
from tkinter.filedialog import askdirectory

# modules for gmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyinputplus as pyin

def ihs_email():

    jobDir = Path(askdirectory())
    job = jobDir.name
    imgDir = jobDir / 'Images'

    if imgDir.is_dir(): #check if Images folder exists
        # check if the Images folder contains product subfolders
        # if os.listdir(imgDir)[1]
        imgNo = len(os.listdir(imgDir))
    else:
        print('Missing: Images folder')
        sys.exit()

    newJobGuideList = []

    def jobDirFind(pattern):
        try:
            return next(jobDir.glob(pattern))
        except StopIteration:
            return None

    if jobDirFind('*Post-production*') != None:
        newJobGuideList.append('the post-production guideline')
    elif jobDirFind('*Shoot Brief*') != None:
        newJobGuideList.append('the shoot brief')

    if jobDirFind('*Retouch Note*') != None:
        newJobGuideList.append('the retouch note')

    if jobDirFind('*ref*') != None:
        # refNo = len(os.listdir(jobDir / 'ref'))
        newJobGuideList.append('the reference images')

    if len(newJobGuideList) > 1:
        newJobGuideList[-1] = 'and ' + newJobGuideList[-1]
    newGuides = ', '.join(newJobGuideList)

    amendJobGuideList = []

    if jobDirFind('*feedback*') != None:
        amendJobGuideList.append('the feedback pdf')

    if jobDirFind('*Retouch Note*') != None:
        amendJobGuideList.append('the retouch note')

    if jobDirFind('*ref*') != None:
        # refNo = len(os.listdir(jobDir / 'ref'))
        amendJobGuideList.append('the reference images')

    if len(amendJobGuideList) > 1:
        amendJobGuideList[-1] = 'and ' + amendJobGuideList[-1]
    amendGuides = ', '.join(amendJobGuideList)

    newJob = f"Hi,\n\nPlease note that {job} is being uploaded to the server, including {imgNo} images along with {newGuides}. Let me know if there is any question. Thanks!\n\n"

    amendJob = f"Hi,\n\nPlease note that there are amendments required, which are being uploaded to the server under the folder {job}, including {imgNo} images along with {amendGuides}. Let me know if there is any question. Thanks!\n\n"

    if 'Amendment' in str(jobDir):
        emailMSG = amendJob
    else:
        emailMSG = newJob

    # prompt for password
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
        emailSubInput.send_keys(job)

        time.sleep(1)

        emailMSGInput = driver.find_element(By.XPATH, '//*[@id=":r8"]')
        emailMSGInput.send_keys(emailMSG)
    except:
        print('autoEmail Failed!')

if __name__ == '__main__':
        ihs_email()
