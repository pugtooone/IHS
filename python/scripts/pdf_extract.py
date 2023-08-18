#! python3
# 1.0.3 formatting

import io
import os
import sys
from pathlib import Path
from tkinter.filedialog import askopenfilename

import fitz
import pyperclip
from pprint import pprint
from PIL import Image

def img_extract():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    print('img_extract() running...')

    Path.mkdir(file.parent / 'Images', exist_ok=True)
    os.chdir(file.parent / 'Images')

    no_of_img = 0
    for pageNo in range(len(pdf)):
        page = pdf[pageNo]

        # text = page.get_text()
        # # get_text() returns string, need split at newline and convert to list
        # imgNameList = list(text.split('\n'))

        for imgIndex, img in enumerate(page.get_images()):
            xref = img[0]
            baseImg = pdf.extract_image(xref)
            imgBytes = baseImg['image']
            # imgExt = baseImg['ext']
            
            image = Image.open(io.BytesIO(imgBytes))
            #save img with the filename underneath
            # image.save(open(f"{imgNameList[imgIndex]}", "wb"))
            image.save(open(f"{pageNo}-{imgIndex}.png", "wb"))
            no_of_img += 1
            print(f'saving images: {pageNo}-{imgIndex}.png')

    print(f'\n------Summary------\nTotal pages: {len(pdf)}\nTotal images: {no_of_img}')

def all_text_extract():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    text = ""

    for pageNo in range(len(pdf)):
        page = pdf[pageNo]

        text += page.get_text()

    pyperclip.copy(text)
    print('Text copied')

def make_text(words):
    """Return textstring output of get_text("words").
    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0])  # sort by horizontal coordinate
    for w in words:  # fill the line dictionary
        y1 = round(w[3], 1)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return "\n".join([" ".join(line[1]) for line in lines])

def highlight_text_extract():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    text = ""
    drawingCount = 0

    for pageNo in range(len(pdf)):
        page = pdf[pageNo]

        drawings = page.get_drawings()
        for i in range(len(drawings)):
            drawingCount += 1
            rect = drawings[i]['rect']
            # coorList = list(coor)
            # text += page.get_textbox(coorList)

            words = page.get_text("words")
            mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
            filename = make_text(mywords)
            if filename != '':
                text += f'\r {filename}'

    pyperclip.copy(text)
    print('Text copied')
    print(f'Total Selection: {drawingCount}')

def CF_highlight_text_extract():
    """extract high-lighted text from Creative Force contact sheet
    """
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    print(''.center(100,"="))
    print('Scanning for highlighted text...'.center(100) + '\n')

    text = ""
    drawingCount = 0

    for pageNo in range(len(pdf)):
        print(f'Accessing Page [{pageNo + 1}]...')
        page = pdf[pageNo]

        drawings = page.get_drawings()
        for i in range(len(drawings)):
            rect = drawings[i]['rect']
            #continue the loop if the fill colour is white (only return the highlighted one)
            if drawings[i]["fill"] == (1.0, 1.0, 1.0):
                continue
            drawingCount += 1

            try:
                filename = page.get_text("words", clip=rect)[0][4]
                if filename.endswith('tif'):
                    text += f'\n{filename}'
            except IndexError:
                print(f"Error: No words extractable for {rect}")

    pyperclip.copy(text)
    print('Text copied')
    print(f'Total Selection: {drawingCount}')

def main():
    while True:
        print('''Choose the digital assets to extract from PDF: 

    [1]: All Text
    [2]: High-lighted Text
    [3]: Creative Force High-lighted Text
    [4]: Images
            ''')
        answer = input()
        if answer == '1':
            all_text_extract()
            sys.exit()
        elif answer == '2':
            highlight_text_extract()
            sys.exit()
        elif answer == '3':
            CF_highlight_text_extract()
            sys.exit()
        elif answer == '4':
            img_extract()
            sys.exit()

if __name__ == "__main__":
    main()
