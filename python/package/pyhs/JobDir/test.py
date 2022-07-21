from pathlib import Path
from tkinter.filedialog import askdirectory
from ToSend import ToSend

def main():
    jobFolder = Path(askdirectory())
    toSendFolder = ToSend(jobFolder)
    toSendFolder.get_email()

if __name__ == '__main__':
    main()
