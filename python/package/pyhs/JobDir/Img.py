import os

class Img:
    def __init__(self, directory):
        """
        initialize ImgList obj
        Parameter: Path obj of JobDir
        """
        self.imgDir = directory / 'Images'
        self.imgList = os.listdir(self.imgDir)
        self.imgNum = len(self.imgList)
