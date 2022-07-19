from pathlib import Path
import pickle


class General():#General Function and Data
    #Dirs Defination
    
    sendoutdir = Path().home() / 'Desktop' / 'Send Out'
    qcdir =  Path().home() / 'Desktop' / 'Waiting QC'
    
    #Brands' Specification
    brands = {"general":{"dir":"General","spec":[2000,2000,300,1],"vendor":"Dresma"},
            "onthelist":{"dir":"OnTheList","spec":[2000,2000,300,1],"vendor":"CutOut"}
            }
    

    #------------------------------------------------------------
    @classmethod
    def setUp(cls,state:str,brand):
        if state == 'sendout':
            if cls.sendoutdir.is_dir() == False:
                cls.sendoutdir.mkdir(exist_ok=False)
                
        if state == 'qc':
            if cls.qcdir.is_dir() == False:
                cls.qcdir.mkdir(exist_ok=False)
                
    @classmethod
    def newBrand(cls,brand:str,dir:str,spec:list,vendor:str):
        newbrand = {f"{brand}":{"dir":f"{dir}","spec":spec}}
        cls.brands.update(newbrand)
    
    @classmethod
    def countImg(cls,brand:str):
        workingbranddir = cls.brands[brand]["dir"]
        countdir = Path(f"{cls.sendoutdir} / {workingbranddir}")
        imagelist = []
        imagelist.append(countdir.glob("*.jpg"))
        imagelist.append(countdir.glob("*.png"))
        imagelist.append(countdir.glob("*.tif"))
        return len(imagelist)
        
    def newjobdir(self):
        pass
    
    def emailgen(self):
        pass
    
class SendOut(General):
    def __init__(self, brand = "general", vendor = "cutout"):
        self.brand = brand
        self.vendor = vendor
        super().setUp("sendout")
        brand = super().brands.get(brand)
        
        
    
    def sendout(self):
        super().countImg("SendOut")
        
class QC(General):
    def __init__(self):
        pass
    
if __name__ == "__main__":
    pass