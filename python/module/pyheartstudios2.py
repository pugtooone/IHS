from pathlib import Path

class General():#General Function and Data
    #Dirs
    sendoutdir = Path().home() / 'Desktop' / 'Send Out'
    qcdir =  Path().home() / 'Desktop' / 'Waiting QC'
    #Brands' Specification
    brands = {"general":{"dir":"General","spec":[2000,2000,300,1]},
              "onthelist":{"dir":"OnTheList","spec":[2000,2000,300,1]}
              }
    
    
    
    #------------------------------------------------------------
    @classmethod
    def setUp(cls,state:str):
        if state == 'sendout':
            if cls.sendoutdir.is_dir() == False:
                cls.sendoutdir.mkdir(exist_ok=False)
                
        if state == 'qc':
            if cls.qcdir.is_dir() == False:
                cls.qcdir.mkdir(exist_ok=False)
    @classmethod
    def newBrand(cls,brand,dir,spec:list):
        newbrand = {f"{brand}":{"dir":f"{dir}","spec":spec}}
        cls.brands.update(newbrand)
        
    def countImg(self):
        pass
    
    def newjobdir(self):
        pass
    
class SendOut(General):
    def __init__(self, brand = "general", vendor = "cutout"):
        self.brand = brand
        self.vendor = vendor
        super().setUp('sendout')
        brand = super().brands.get("general")
        
    
    def send():
        super().setUp()
        
class QC(General):
    def __init__(self):
        pass
    
if __name__ == "__main__":
    pass