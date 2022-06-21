#! python3
# copy email template to the clipboard

# version:
# 1.3.1: fix IndexError for empty GuideList

# plan: 
# 1) paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

import sys, os
import pyperclip
from pathlib import Path
from tkinter.filedialog import askdirectory

"""
# modules for gmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
"""

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
        pyperclip.copy(amendJob)
        print(f'Amendment job [ {job} ] Email template copied to the clipboard')
    else:
        pyperclip.copy(newJob)
        print(f'New job [ {job} ] Email template copied to the clipboard')

    # prompt for password
    """
    ac = "zeric.chan@ihearstudios.com"
    pw = getpass("Enter Password: ")

    try:
        driver = webdriver.Chrome()
        driver.get('https://mail.google.com/mail/u/0/#inbox')

        acInput = driver.find_element(By.ID, 'identifierId')
        acInput.send_keys(ac)

        nextButton = driver.find_element(By.ID, 'identifierNext')
        nextButton.click()

        pwInput = driver.find
    """

if __name__ == '__main__':
        ihs_email()
