from PIL import Image
import os

class Img:
    def __init__(self, directory):
        """
        initialize ImgList obj
        Parameter: Path obj of JobDir
        """
        self.imgDir = directory / 'Images'

    def get_img_list(self):
        self.imgList = os.listdir(self.imgDir)
        return self.imgList

    def get_img_num(self):
        self.imgNum = len(self.imgList)
        return self.imgNum

    def check_img_spec(self):
        for img in self.imgList:
            imgPath = self.imgDir / img
            imgObj = Image.open(imgPath)
