from Img import Img
from Doc import Doc

class JobDir:
    def __init__(self, directory):
        """
        initialize JobDir obj
        Parameter: Path obj of JobDir
        """
        self.jobDir = directory
        self.jobName = directory.name
        self.imgObj = Img(self.jobDir)
        self.imgNum = self.imgObj.get_img_num()
        self.docObj = Doc(self.jobDir)
        self.docList = self.docObj.get_doc_list()
        self.docItems = self.docObj.get_doc_items()

    def get_doc(self):
        return self.docList

    def get_img_no(self):
        return self.imgNum

    def check_img_spec(self):
        pass
