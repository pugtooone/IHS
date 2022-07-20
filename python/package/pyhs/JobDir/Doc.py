import os

class Doc:
    def __init__(self, directory):
        """
        initialize DocList obj
        Parameter: Path obj of JobDir
        """
        self.docDir = directory / 'Documents'
        self.docList = os.listdir(self.docDir)
