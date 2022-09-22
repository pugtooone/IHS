import os
from PIL import Image
import tkinter as tk
from tkinter import END, LEFT, RIGHT, filedialog
'''------------------------------------------------------------------------------------------------------------------------'''
resolist =[]
list = []
finallist = []

def findtrans():
    cleartext()
    path =  filedialog.askdirectory(title= "Select Directory",initialdir='*/Desktop/')
    os.chdir(path)
    global lb2
    lb2 = tk.Label()
    lb2.grid(column=3,row=6)
    i = 0
    for file in os.listdir(path):
        if file.endswith('.tif') or file.endswith('.png'):
            try:
                
                lb2.config(text = f'{file}')
                win.update()
                image = Image.open(file).convert('RGBA')
                width,height = image.size
                alpha_range = image.getextrema()[-1]
                

                if width != 2325 or height != 3100:
                    resolist.append(file)
                if 'MO-ST' not in file:
                    if alpha_range == (255,255):
                        list.append(file)
                i += 1

            except KeyboardInterrupt:
                print("Stopped")

    for file in list:
        if 'FL-ST-D' not in file:
            finallist.append(file)

    for name in finallist:
        et1.insert(tk.END, "OR name:" + name +'\n')

    for name in resolist:
        et2.insert(tk.END, "OR name:" + name +'\n')

    
    lb4.config(text=str(i))
    lb2.grid_remove()
    win.update()


def cleartext():
    lb4.config(text='')
    list.clear()
    finallist.clear()
    resolist.clear()
    et1.delete('1.0',END)
    et2.delete('1.0',END)

'''---------UI------------'''

win = tk.Tk()

win.title("Transparent Checker")


global lb4
global et1
global et2
frame1 = tk.Frame(win)
et1 = tk.Text(frame1,height = 12)
et2 = tk.Text(frame1,height=12)
lb1 = tk.Label(text=' is not transparent!')
lb3 = tk.Label(text = 'Wrong Resolution')
bt1 = tk.Button(text='Cancel',command = lambda:win.destroy())
global bt2 
bt2 = tk.Button(text='Choose Directory',command = lambda:findtrans())
bt3 = tk.Button(text='Clear',command=lambda:cleartext())
lb4 = tk.Label()
    

frame1.grid(column=1,row=1,columnspan=3)
et1.pack(side=LEFT)
et2.pack(side=RIGHT)
lb1.grid(column=1,row=4)
lb3.grid(column=3,row=4)
lb4.grid(column=2,row=4)

bt1.grid(column=1,row =5,sticky='SW')
bt2.grid(column=3,row =5,sticky='SE')
bt3.grid(column=2,row=5,sticky='S')



win.mainloop()