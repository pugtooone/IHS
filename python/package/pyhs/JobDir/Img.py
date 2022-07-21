from PIL import Image
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

    def check_img_spec(self):
        for img in self.imgList:
            imgPath = self.imgDir / img
            imgObj = Image.open(imgPath)
