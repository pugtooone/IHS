import os, re
import pyautogui as pya
import tkinter as tk

if not os.path.isdir('Check'):
    os.mkdir('Check')
    pya.alert(title = 'Ralph Lauren Name Checker Beta 1.0', text = 'Please put the images in the newly generated "Check" Folder.')

path = "/Users/IvanChan/Desktop/Ralph-Lauren-Checker-main/Check"
#path = pya.prompt(text= 'Please copy pathname to the prompt' ,default="Check/")
cor_name =[]

bag_cor_name = ['BagFront','BagSide','BagBack','BagInterior','BagDetail1','BagDetail2','BagReversible','BagAngle','BagFrontOpen']
flat_cor_name = ['laydown'.upper(),'laydownback'.upper(),'SL-Detail1']
shoes_cor_name = ['ShoesAngle','ShoesOverhead','ShoesBack','ShoesProfile']
tt_cor_name = ['TableTop','TT-Detail1','TableTop'.upper(),'tt-detail1'.upper()]
bust_cor_name = ['BustBack','Bust_Insert','Bust_Front','Bust','BustBack'.upper(),'Bust_Insert'.upper(),'Bust_Front'.upper(),'bust'.upper()]
newfile = []
wrong = []
uniquelist = []
checknumlist = []
cor_name.extend(bag_cor_name)
cor_name.extend(flat_cor_name)
cor_name.extend(shoes_cor_name)
cor_name.extend(tt_cor_name)
cor_name.extend(bust_cor_name)



possible_comp_number = []

for single in cor_name:
    for i in range(1,10):
        extens = f"_Comp{i}"
        new_all = str(single) + str(extens)
        possible_comp_number.append(new_all)
        new_all = str(single) + str(extens).upper()
        possible_comp_number.append(new_all)
        
cor_name.extend(possible_comp_number)




'''-----------------------------------------------------------------------------------------------'''

os.chdir(path)
for file in os.listdir():
    extractname = re.split('_',file,1)
    print(extractname)
    if len(extractname) < 2:
        wrong.append(extractname[0])
    else:
        if extractname[1].endswith('.png') or extractname[1].endswith('.tif')  or extractname[1].endswith('.jpg') or extractname[1].endswith('.jpeg'):
            newextractname = re.sub(r".{4}$","",extractname[1]) 
            newfile.append([extractname[0],newextractname])


for file in newfile:
    if file[1] not in cor_name:
        #x = file[0]+ "_" + file[1] + " is wrong!"
        x = file[0] + "_" + file[1]
        wrong.append(x)

for file in newfile:
    if file[0] not in uniquelist:
        uniquelist.append(file[0])
        checknumlist.append(file)


    


win = tk.Tk()

win.title("Ralph Lauren Name Checker Beta 1.0")

et1 = tk.Text(height = 20)
for name in wrong:
    et1.insert(tk.END, 'OR name:' + name +'\n')
et2 = tk.Text(height = 20)
lb1 = tk.Label(text=' is wrong!')
bt1 = tk.Button(text='Cancel',command = lambda:win.destroy())
bt2 = tk.Button(text = 'Change Name(WIP)' ,state='disable')

et1.grid(column=1,row=1,rowspan=3,columnspan=3)
el2.grid(column=4,row=1,rowspan=3,columnspan=3)
lb1.grid(column=3,row=4)
bt1.grid(column=2,row =5)
bt2.grid(column=4,row =5)


win.mainloop()