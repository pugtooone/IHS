#! python3
# copy email template to the clipboard

# version:
# 1.2.0: fix 

# plan: 
# 1) paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

def ihs_email():
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

    def jobDirFind(pattern):
        try:
            next(jobDir.glob(pattern)).exists()
        except StopIteration:
            pass

    if jobDirFind('*Post-production*'):
        newJobGuideList.append('the post-production guideline')
    elif jobDirFind('*Shoot Brief*'):
        newJobGuideList.append('the shoot brief')

    if jobDirFind('*Retouch Note*'):
        newJobGuideList.append('the retouch note')

    if jobDirFind('*ref*'):
        # refNo = len(os.listdir(jobDir / 'ref'))
        newJobGuideList.append('the reference images')

    newJobGuideList[-1] = 'and ' + newJobGuideList[-1]
    newGuides = ', '.join(newJobGuideList)

    amendJobGuideList = []

    if jobDirFind('*feedback*'):
        amendJobGuideList.append('the feedback pdf')

    if jobDirFind('*Retouch Note*'):
        amendJobGuideList.append('the retouch note')

    if jobDirFind('*ref*'):
        # refNo = len(os.listdir(jobDir / 'ref'))
        amendJobGuideList.append('the reference images')

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

if __name__ == '__main__':
    ihs_email()
