from Img import Img
from Doc import Doc
from pathlib import Path
import os, sys

class JobDir:
    # class attributes
    brandBaseDir = Path('/Volumes/Studio/CLIENTS/')
    brandBase = os.listdir(brandBaseDir)

    def __init__(self, directory):
        """
        initialize JobDir obj
        Parameter: Path obj of JobDir
        """
        JobDir.check_dir_structure(directory)
        self.jobDir = directory
        self.jobName = directory.name
        self.imgDirObj = Img(self.jobDir)
        self.docDirObj = Doc(self.jobDir)

    @classmethod
    def check_dir_structure(cls, directory):
        jobDirls = os.listdir(directory)
        if 'Images' in jobDirls and 'Documents' in jobDirls:
            pass
        else:
            #could change to return boolean, then a restructure function
            print('Error: wrong folder structure')
            sys.exit(2)

    def get_brand(self):
        for brand in JobDir.brandBase:
            if brand in self.jobName:
                return brand

    def get_img_list(self):
        self.imgDirObj.get_img_list()

    def get_img_num(self):
        self.imgDirObj.get_img_num()

    def get_doc_list(self):
        self.docDirObj.get_doc_list()

    def get_doc_items(self):
        self.docDirObj.get_doc_items()

    def check_img_spec(self):
        self.imgDirObj.check_img_spec(self.get_brand())
