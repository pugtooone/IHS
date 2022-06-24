#! python3

from logging import root
import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askopenfilename
from PyPDF2 import PdfReader

def choose_pdf():
    pdfFile = Path(askopenfilename())
    return pdfFile

def tkWindow(script):
    root = tk.Tk()
    root.geometry('200x300+100-100')
    root.attributes('-topmost', True)

    pdfButt = tk.Button(root, text='Select PDF to process', width=15, height=5, command=script)
    pdfButt.pack(padx=10, pady=10)
    root.mainloop()

def root_destroy():
    global root
    root.destroy()

def pdf_parser(file):
    pdf = PdfReader(file)

    totalPages = pdf.getNumPages()

    for i in range(0,totalPages - 1):
        page = pdf.pages[i]
        print(page.extract_text())

if __name__ == '__main__':
    tkWindow(pdf_parser(choose_pdf()))
    root_destroy()
