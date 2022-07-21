from JobDir import JobDir
import pyperclip

class ToSend(JobDir):
    def __init__(self, directory):
        super().__init__(directory)

    def get_email(self):
        self.email = f'Hi!\n\nPlease note that {self.jobName} is being uploaded to the server, including {self.imgNum} images along with {self.docItems}. Let me know if there is any question. Thanks!\n\n'
        pyperclip.copy(self.email)
        print('email template copied')
