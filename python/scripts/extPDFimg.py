#! python3

from pathlib import Path
from tkinter.filedialog import askopenfilename
from PIL import Image
import fitz, io, os

def main():
    file = Path(askopenfilename())
    pdf = fitz.open(file)

    Path.mkdir(Path.cwd() / 'Images')
    os.chdir(Path.cwd() / 'Images')

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

if __name__ == "__main__":
    main()
