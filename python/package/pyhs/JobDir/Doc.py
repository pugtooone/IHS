import os

class Doc:
    def __init__(self, directory):
        """
        initialize DocList obj
        Parameter: Path obj of JobDir
        """
        self.docDir = directory / 'Documents'
        self.docListDir = os.listdir(self.docDir)

    # globbing pattern for counting the documents, which is universal to all instances: {'pattern to search for': 'document'}
    docPattern = {'*Post-production*': 'post-production guideline', '*Shoot Brief*': 'shoot brief', '*Retouch Note*': 'retouch note', '*Swatch*': 'swatches', '*Overlay*': 'overlay', '*Feedback*': 'feedback.pdf'}

    def get_doc_list(self):
        """
        create a dictionary that store the instances of documents
        """
        self.docList = []
        # append the documents(values) to the docList(list), if pattern(keys) present
        for pattern, doc in self.docPattern.items():
            if self._doc_glob(pattern):
                self.docList.append(doc)
        return self.docList

    def _doc_glob(self, pattern):
        """
        internal pattern search method for get_doc_list()
        could change to re for case-insensitive matching
        """
        try:
            return next(self.docDir.glob(pattern))
        except StopIteration:
            return None