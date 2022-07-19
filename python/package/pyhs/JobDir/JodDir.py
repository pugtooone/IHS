from pathlib import Path
import os, ImgList

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
        pass

    def get_img_no(self):
        return ImgList.imgNum

    def check_img_spec(self):
        pass
