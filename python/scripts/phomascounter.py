import tkinter as tk
import time



activate = 0
t = ""
et = ""
i = 0

main = tk.Tk()
main.title("Phomas Counter")
main.attributes('-topmost', True)


def addcounter():
    global t
    global i
    i += 1
    lb1.config(text=str(i) + "\n " + t)
    lb1.update()

def minuscounter():
    global i
    i -= 1
    lb1.config(text=str(i) + "\n " + t)
    lb1.update()

def start():
    global activate, t ,et ,i
    
    if activate == 0:
        i=0
        t = time.asctime()
        lb1.config(text = str(i) +"\n  "+ t )
        lb1.update()
        bt3.config(text="Stop")
        bt3.update()
        activate = 1
        return None
        
        
    if activate == 1:
        et = time.asctime()
        lb1.config(text = str(i) +"\n  "+ t +"\n  "+ et)
        bt3.config(text="Start")
        lb1.update()
        bt3.update()
        activate=0
        return None



bt1 = tk.Button(height = 5,width = 15,command=addcounter,text="+" )
bt2 = tk.Button(height = 5,width = 15,command=minuscounter,text="-")
bt3 = tk.Button(height = 5,width = 15,command=start,text="start")
lb1 = tk.Label(text="0",height=5,font=("Roboto","20"))

lb1.pack(pady=5)
bt3.pack(pady=5)
bt1.pack(pady=5)
bt2.pack(pady=5)

main.mainloop()