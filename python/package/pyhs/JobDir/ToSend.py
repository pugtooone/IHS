from JobDir import JobDir
import pyperclip

class ToSend(JobDir):
    def __init__(self, directory):
        super().__init__(directory)

    def write_email(self):
        self.imgNum = self.get_img_num()
        self.docItems = self.get_doc_items()
        self.email = f'Hi!\n\nPlease note that {self.jobName} is being uploaded to the server, including {self.imgNum} images along with {self.docItems}. Let me know if there is any question. Thanks!\n\n'
        pyperclip.copy(self.email)
        print('email template copied')
        return self.email

    def check_img_spec(self):
        self.imgDirObj.check_img_spec('ToSend')
