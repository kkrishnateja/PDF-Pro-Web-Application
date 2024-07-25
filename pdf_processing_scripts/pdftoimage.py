# from pdf2image import convert_from_path
# pages=convert_from_path('image.pdf',500)

# for num,page in enumerate(pages):
#     page.save('page'+str(num)+'.jpg','JPEG')
    

import os
import shutil
from pdf2image import convert_from_path

def pdf_img_func(pdffile):
    # Define the directory to save images
    output_dir = 'pdf_imgs'

    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # Remove existing images in the directory
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    # Convert PDF to images
    pages = convert_from_path(pdffile, 500)

    # Save images to the directory
    for num, page in enumerate(pages):
        page.save(os.path.join(output_dir, f'page{num}.jpg'), 'JPEG')

# pdf_img_func("sample.pdf")
