#! python3

from logging import root
import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askopenfilename
from PyPDF2 import PdfReader

def choose_pdf():
    pdfFile = Path(askopenfilename())
    return pdfFile


def pdf_parser():
    pdf = PdfReader(pdfFile)

    totalPages = pdf.getNumPages()

    for i in range(0,totalPages - 1):
        page = pdf.pages[i]
        print(page.extract_text())

def main():
    root = tk.Tk()
    root.geometry('200x300+100-100')
    root.attributes('-topmost', True)

    pdfButt = tk.Button(root, text='Select PDF to process', width=15, height=5, command=choose_pdf)
    pdfButt.pack(padx=10, pady=10)
    root.mainloop()
    root.destroy()

if __name__ == '__main__':
    pdf_parser(choose_pdf())
