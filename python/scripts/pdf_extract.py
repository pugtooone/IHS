#! python3
# 1.0.2 introduce text_extract()

from pathlib import Path
from tkinter.filedialog import askopenfilename
from PIL import Image
import fitz, io, os, sys, pyperclip

def img_extract():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    Path.mkdir(file.parent / 'Images')
    os.chdir(file.parent / 'Images')

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
            image.save(open(f"{imgIndex}.png", "wb"))

    print('Images copied')

def text_extract():
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

def select_text_extract():
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

def main():
    while True:
        print('Extract [All Text] or [Selected Text] or [Images] from PDF?')
        answer = input()
        if answer.lower() == 'images':
            img_extract()
            sys.exit()
        elif answer.lower() == 'all text':
            text_extract()
            sys.exit()
        elif answer.lower() == 'selected text':
            select_text_extract()
            sys.exit()

if __name__ == "__main__":
    main()
