'''
Finds all text in all pdfs in the source_pdfs directory and saves it to 
one json file per pdf at `found txt/*.json`

Uses tesseract OCR.
'''

#%%

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import tqdm 
from glob import glob
import json
import os

out_dir = 'found txt'

def get_all_text(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # List to store the text from each page
    ocr_text_per_page = []

    # Iterate over each page in the PDF
    for page_num in tqdm.tqdm(range(len(pdf_document)), desc='file '+os.path.basename(pdf_path)):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Get the page as a PNG image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Perform OCR on the image
        text = pytesseract.image_to_string(img, lang='heb')  # Use lang='heb' for Hebrew text

        # Append the text to the list
        ocr_text_per_page.append(text)

    json.dump(ocr_text_per_page,
              open(os.path.join(out_dir, os.path.basename(pdf_path).replace('.pdf', '.json')), 'w')
              )
    
    return ocr_text_per_page


all_text = {pdf_path: get_all_text(pdf_path) 
            for pdf_path in  glob('source_pdfs/*.pdf')}
