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
        self.docObj = Doc(self.jobDir)

    def get_doc(self):
        self.docList = self.docObj.get_doc_list()
        return self.docList

    def get_img_no(self):
        self.imgNum = self.imgObj.get_img_num()
        return self.imgNum

    def check_img_spec(self):
        pass
