from Img import Img
from Doc import Doc
from pathlib import Path
import os

class JobDir:
    # universal attributes
    brandBaseDir = Path('/Volumes/Studio/CLIENTS/')
    brandBase = os.listdir(brandBaseDir)

    def __init__(self, directory):
        """
        initialize JobDir obj
        Parameter: Path obj of JobDir
        """
        self.jobDir = directory
        self.jobName = directory.name
        self.brand = self._brand_search()

        self.imgObj = Img(self.jobDir)
        self.imgList = self.imgObj.imgList
        self.imgNum = self.imgObj.imgNum

        self.docObj = Doc(self.jobDir)
        self.docList = self.docObj.docList
        self.docItems = self.docObj.get_doc_items()

    def _brand_search(self):
        for brand in JobDir.brandBase:
            if brand in self.jobName:
                return brand

    def check_img_spec(self):
        pass
