#! python3
# copy email template to the clipboard

# version:
# 1.0.0: first stable release with auto-fill function

# plan: 
# 1) paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

import sys, os
import pyperclip
from tkinter.filedialog import askdirectory
from pathlib import Path

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

if jobDir.glob('*Post-production*'):
    newJobGuideList.append('the post-production guideline')
elif jobDir.glob('*Shoot Brief*'):
    newJobGuideList.append('the shoot brief')

if jobDir.glob('*Retouch Note*'):
    newJobGuideList.append('the retouch note')

if jobDir.glob('*ref*'):
    # refNo = len(os.listdir(jobDir / 'ref'))
    newJobGuideList.append('the reference images')

newJobGuideList[-1] = 'and ' + newJobGuideList[-1]
newGuides = ', '.join(newJobGuideList)

amendJobGuideList = []

if jobDir.glob('*feedback*'):
    amendJobGuideList.append('the feedback pdf')

if jobDir.glob('*Retouch Note*'):
    amendJobGuideList.append('the retouch note')

if jobDir.glob('*ref*'):
    # refNo = len(os.listdir(jobDir / 'ref'))
    amendJobGuideList.append('the reference images')

amendJobGuideList[-1] = 'and ' + amendJobGuideList[-1]
amendGuides = ', '.join(amendJobGuideList)

newJob = """Hi,\n\nPlease note that %s is being uploaded to the server, including %s images along with %s. Let me know if there is any question. Thanks!\n\n""" % (job, imgNo, newGuides)

amendJob = """Hi,\n\nPlease note that there are amendments required, which are being uploaded to the server under the folder %s, including %s images along with %s. Let me know if there is any question. Thanks!\n\n""" % (job, imgNo, amendGuides)

if 'Amendment' in str(jobDir):
    pyperclip.copy(amendJob)
else:
    pyperclip.copy(newJob)
