'''
Finds all text in all pdfs in the source_pdfs directory and saves it to a json file all_text.json.

Uses tesseract OCR.
'''

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import tqdm 
from glob import glob
import json


# Path to your PDF file
pdf_path = 'source_pdfs/אסא.pdf'


def get_all_text(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # List to store the text from each page
    ocr_text_per_page = []

    # Iterate over each page in the PDF
    for page_num in tqdm.tqdm(range(len(pdf_document))):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Get the page as a PNG image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Perform OCR on the image
        text = pytesseract.image_to_string(img, lang='heb')  # Use lang='heb' for Hebrew text

        # Append the text to the list
        ocr_text_per_page.append(text)

    return ocr_text_per_page

all_text = {pdf_path: get_all_text(pdf_path) for pdf_path in glob('source_pdfs/*.pdf')}
json.dump(all_text, open('all_text.json', 'w'))
