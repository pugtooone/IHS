from glob import glob
import os

class FileManagement():
    userpath = ''

    @classmethod
    def initialize(self):
        workdir = os.path.join(self.userpath,'Batch For Vendor')
        if os.path.exists(workdir) == False:
            os.mkdir(workdir)
            #os.makedirs(os.path.join(workdir,'OnTheList'))
            #os.makedirs(os.path.join(workdir,'Kipling'))#Check everytimes when creating a job is much better
        else:
            print('directory exist!')

    @classmethod
    def setPath(self,path):
        self.userpath = path
    
    @classmethod
    def getCount(self):
        if self.userpath != None:
            try:
                images = len(glob(f'{self.userpath}/*'))
                if images == 0:
                    print('Is the directory not exist? Or the path is wrong?')
                else:
                    return images

            except FileNotFoundError as F:
                print(F)

    def newJob(self,job,jobtype):
        if self.userpath != None:
            newpath = os.path.join(self.userpath,jobtype)
            os.mkdir(os.path.join(newpath,str(job)))


def msgGenerate(job, imgcount, ppg):
    imgcount = str(imgcount)
    return f'Hi,\n please note that {job} is being uploaded to the server, with {imgcount} images and the post-production guideline.\n let us know if there is any question, thank you very much.'

#think about what function you need in this app?
'''get jobs in gspreadsheet
   find deadline provide selection to the user
   open new folder

'''
class ImageCheck():
    dimension = ()
    ppi = None
    cprofile = None

    @classmethod
    def setImageSpec(self, dimension:tuple,ppi:int,cprofile:int):
        if isinstance(dimension,tuple):
            self.dimension = dimension
        else:
            raise TypeError('The value type of dimension should be tuple')
        self.ppi = ppi
        self.cprofile = cprofile

    @classmethod
    def checkSpec(self,dimension,ppi,cprofile):
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
    
