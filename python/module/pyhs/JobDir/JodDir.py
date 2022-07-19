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

    def get_doc(self):

    def get_img_no(self):
        len(ImgList.imgList)

class ImgList:
    def __init__(self, directory):
        """
        initialize ImgList
        Parameter: Path obj of JobDir
        """
        self.imgDir = directory / 'Images'
        self.imgList = os.listdir(self.imgDir)
