from PIL import Image
from pathlib import Path
import sys, json

class Img:
    def __init__(self, directory):
        """
        initialize ImgList obj
        Parameter: Path obj of JobDir
        """
        self.imgDir = directory / 'Images'
        self.imgListIter = self.imgDir.glob('*') #Iterator for img

    def get_img_list(self):
        self.imgList = list(self.imgListIter)
        return self.imgList

    def get_img_num(self):
        self.imgNum = len(self.imgList)
        return self.imgNum

    def check_img_spec(self, brand):
        Img.brandJsonFile = open('Resources/BrandDatabase.json')
        Img.brandJson = json.load(Img.brandJsonFile)
        Img.brandData = Img.brandJson[brand]

        for img in self.imgListIter:
            imgObj = Image.open(img)

            for k, v in Img.brandData.items():
                if eval(f'imgObj.{k}') != v:
                    print('Error: Wrong Image Spec')
                    sys.exit(2)
            
            imgObj.close()

        Img.brandJsonFile.close()
        print('All Images Checked')
