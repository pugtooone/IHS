from glob import glob
import os,re
from pathlib import Path


class FileManagement():
    
    def __init__(self,jobtype:str):
        self.wdir =  Path.home() / 'Batch for Vendor' #Define main folder path
        if self.wdir.is_dir() == False:
            os.mkdir(self.wdir)

        self.jobdir = self.wdir / jobtype# create pathname as object
        self.jobdir.mkdir()
        

    
    #Get Image Count from user-defined path
    def getCount(self) -> int:
        """
        Run initialize() first to set path
        Parameters: None
        Return: Count of image
        """
        if self.userpath != None:
            try:
                imagecount = len(glob(f'{self.userpath}/*.*'))
                if imagecount == 0:
                    raise ValueError("Can't find any images")
                    
                else:
                    return imagecount

            except FileNotFoundError as F:
                print(F)

    def newJob(self,job:int,jobtype:str):
        if self.userpath != None:
            newpath = os.path.join(self.userpath,jobtype)
            os.mkdir(os.path.join(newpath,str(job)))

    def rename(self,):
        '''
        Rename recursively
        '''
        pass

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
    
