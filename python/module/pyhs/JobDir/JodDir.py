from pathlib import Path
import os

class JobDir:
    def __init__(self, directory):
        """
        initialize JobDir obj
        Parameter: Path obj of JobDir
        """
        self.jobDir = directory
        self.jobName = directory.name
        self.imgList = os.listdir(self.jobDir / 'Images')

    def get_doc(self):

    def get_img_no(self):
        return len(self.imgList)

    def check_img_spec(self):
