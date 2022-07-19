from glob import glob
import os,re
from pathlib import Path
#File structure variable wdir(Batch For Vendor)/jobdir(OnTheList)/batchdir(OnTheList 000)
class SetUp():
    def __init__(self,brand:str,batchdir:str):
        self.wdir =  Path.home() / 'Desktop' / 'Batch for Vendor' #Define main folder path
        if self.wdir.is_dir() == False:
            os.mkdir(self.wdir)
            
        self.jobdir = self.wdir / brand# create pathname as object, create job folder
        if self.jobdir.is_dir() == False:
            self.jobdir.mkdir()
            
        self.batchdir = self.jobdir / batchdir
        if self.batchdir.is_dir() == False:
            self.batchdir.mkdir()
            
    #Get Image Count from user-defined path
    def getCount(self,batchname:str) -> int:
        """
        Get Image Count by this function
        Parameters: None
        Return: Count of image
        """
        self.batchdir = self.jobdir / batchname
        if self.batchdir.is_dir:
            try:
                imagecount = len(self.batchdir.glob('*.*'))
                if imagecount == 0:
                    raise ValueError("Can't find any images")
                    
                else:
                    return imagecount

            except FileNotFoundError as F:
                print(F)

    def rename(self):
        '''
        Rename recursively
        '''
        pass
    
    #inheritance function
    
    
    def setBatchDir(self,batchname):
        self.batchdir = self.jobdir / batchname
        return self.batchdir

class ToBeSent(SetUp):
    @staticmethod
    def job(brand:str,batchname:str):
        '''Set up job
        Parameters:
        brand(str) : Inputs brand name(e.g. Kipling)
        batchname(str) : Input the name of folder you send out.
        '''
        return SetUp(brand,batchname)
    
    
class Image():
    dimension = ()
    ppi = 300
    cprofile = 1

    def __init__(self,imagepath:str):
        '''Set up Image location'''
        self.imagepath = imagepath
    
    def setImageSpec(self, dimension:tuple,ppi:int = 300,cprofile:int=1) -> list:#0xA001 is the keyword for colorprofile, if (0xA001) == 1 or exif.get(0x0001) == 'R98' then is RGB ref:https://exiftool.org/TagNames/EXIF.html
        '''
        Set up Image Spec

        Parameters:
        dimension (tuple): Width x Height of the image.
        ppi (int): ppi of the image. Default is 300.
        cprofile (int): Color Profile of the image, 1 is sRGB. Default is 1.

        '''
        if isinstance(dimension,tuple):
            self.dimension = dimension
        else:
            raise TypeError('The value type of dimension should be tuple')
        self.ppi = ppi
        self.cprofile = cprofile
        return [self.dimension,self.ppi,self.cprofile]


    def checkSpec(self,dimension:tuple,ppi:int,cprofile:int):
        '''
        Function for checking exif content

        Parameters:
        dimension (tuple):
        '''
        returnflag = {'dimension':1, 'ppi':1, 'cprofile':1}
        if self.dimension != None and self.ppi != None and self.cprofile != None:
            if dimension != self.dimension:
                returnflag.update({'dimension': 0})
            if ppi != self.ppi:
                returnflag.update({'ppi': 0})
            if cprofile != self.cprofile:
                returnflag.update({'cprofile': 0})
            return returnflag
        else:
            raise ValueError('Missing Value of Image Spec')

def main():
    pass

if __name__ == "__main__":
    main()
    
