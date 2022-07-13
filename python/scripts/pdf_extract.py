#! python3
# 1.0.2 introduce text_extract()

from pathlib import Path
from tkinter.filedialog import askopenfilename
from PIL import Image
import fitz, io, os, pyperclip

def img_extract():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    Path.mkdir(file.parent / 'Images')
    os.chdir(file.parent / 'Images')

    for pageNo in range(len(pdf)):
        page = pdf[pageNo]

        text = page.get_text()
        # get_text() returns string, need split at newline and convert to list
        imgNameList = list(text.split('\n'))

        for imgIndex, img in enumerate(page.get_images()):
            xref = img[0]
            baseImg = pdf.extract_image(xref)
            imgBytes = baseImg['image']
            # imgExt = baseImg['ext']
            
            # writing the image and save with the text found (might cause error)
            image = Image.open(io.BytesIO(imgBytes))
            image.save(open(f"{imgNameList[imgIndex]}", "wb"))

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

def main():
    print('Extract [Text] or [Images] from PDF?')
    answer = input()
    if answer == 'Images':
        img_extract()
    elif answer == 'Text':
        text_extract()

if __name__ == "__main__":
    main()
