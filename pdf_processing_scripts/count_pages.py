# PAGE COUNT: #!/usr/bin/python3

# print('Content-type: text/html\r\n\r')

# import fitz
# doc = fitz.open('/uploads/input.pdf')
# print(doc.page_count)

import fitz
import os

def count_pages_func(pdf_filename):
    # Assuming app.py is located in the root directory of your project
    UPLOAD_FOLDER = 'uploads'
    pdf_filename = 'input.pdf'
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    # Check if the file exists before opening it
    if os.path.isfile(pdf_path):
        doc = fitz.open(pdf_path)
        # print(f"Number of pages in {pdf_filename}: {doc.page_count}")
        return doc.page_count
        # Process the document further as needed
    else:
        print(f"File {pdf_filename} not found in {UPLOAD_FOLDER}")
