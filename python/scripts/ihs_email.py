#! python3
# copy email template

# version:
# 1.1.0: restructure the script with OOP

# plan: 
# 1) [cant as id change]paste the draft directly onto the gmail
# 2) [done] parse the job folder, analyse and auto-fill the content of the draft

import sys
from pathlib import Path
import pyperclip
from tkinter.filedialog import askdirectory

class jobDir:
    def __init__(self, path):
        self.path = path

    def get_job_name(self):
        return self.path.name

    def get_img_num(self):
        try:
            imgDir = self.path / 'Images'
            return len(list(imgDir.glob('**/*.tif')))
        except:
            print('Error: Images folder missing')
            sys.exit()

    docPattern={'*Post-production*': 'the post-production guideline', '*Shoot Brief*': 'the shoot brief', '*Retouch Note*': 'the retouch note', '*ref*': 'the reference images', '*feedback*': 'the feedback documents'}

    def get_doc_items(self):
        self.docList = []
        for k, v in jobDir.docPattern.items():
            try:
                if next(self.path.glob(k)):
                    self.docList.append(v)
            except StopIteration:
                return None
        if len(self.docList) > 1:
            self.docItems = ', '.join(self.docList)
        return self.docItems

def main():

    while True:
        path = Path(askdirectory())
        if path == None:
            continue
        else:
            break

    currentJobDir = jobDir(path)
    job = currentJobDir.get_job_name()
    imgNo = currentJobDir.get_img_num()
    docItems = currentJobDir.get_doc_items()
    
    if 'Amendment' in job:
        amendJob = f"Hi,\n\nPlease note that there are amendments required, which are being uploaded to the server under the folder {job}, including {imgNo} images along with {docItems}. Let me know if there is any question. Thanks!\n\n"
        pyperclip.copy(amendJob)
        print(f'Amendment job [ {job} ] Email template copied to the clipboard')
    else:
        newJob = f"Hi,\n\nPlease note that {job} is being uploaded to the server, including {imgNo} images along with {docItems}. Let me know if there is any question. Thanks!\n\n"
        pyperclip.copy(newJob)
        print(f'New job [ {job} ] Email template copied to the clipboard')

if __name__ == '__main__':
    main()
