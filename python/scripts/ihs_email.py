#! python3
# copy email template

# version:
# 2.0.0: autofill gmail new message

# plan: 
# 1) paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

import os
from pathlib import Path
import pyperclip
import tkinter as tk
from tkinter.filedialog import askdirectory

class jobDir:
    def __init__(self, path):
        self.path = path

    def get_job_name(self):
        return self.path.name

    def get_img_num(self):
        try:
            imgDir = self.path / 'Images'
            return len(os.listdir(imgDir))
        except:
            print('Error: Images folder missing')

def main():

    path = Path(askdirectory())
    currentJobDir = jobDir(path)
    job = currentJobDir.get_job_name()
    imgNo = currentJobDir.get_img_num()

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

def tkWindow(script):
    root = tk.Tk()
    root.geometry('300x200+100+100')
    root.attributes('-topmost', True)

    dirButt = tk.Button(root, text='Select Job Folder', width=15, height=5, command=script)
    dirButt.bind('<Button>', root.quit())
    dirButt.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
