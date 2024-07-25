# TEXT EXTRACTOR:                                                                                                                                                                                                     #!/usr/bin/python3

from pypdf import PdfReader
import os

def extract_text_func(pdf_path):
    # Assuming app.py is located in the root directory of your project
    UPLOAD_FOLDER = 'uploads'
    pdf_filename = 'input.pdf'
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    text = ""


    # Check if the file exists before opening it
    if os.path.isfile(pdf_path):
        reader = PdfReader(pdf_path)
        # print(f"There are {len(reader.pages)} pages")
        # Get text from each page
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += page.extract_text()
            # print(f"Page {i+1} text:")
            # print(text)

    
          
        return text

    else:
    # print(f"File {pdf_filename} not found in {UPLOAD_FOLDER}")
        return "File not found"

# print(extract_text_func("sample.pdf"))


# import PyPDF2

# def extract_text_func(pdf_path):
#     reader = PyPDF2.PdfFileReader(pdf_path)
#     print(reader.getDocumentInfo())
#     text = ""
#     for i in range(reader.getNumPages()):
#         text += reader.getPage(i).extract_text()

#     return text
#     # with open("text.txt", "w", encoding='utf-8') as f:
#     #     f.write(text)

# # Example usage:
# # print(extract_text_func('sample.pdf'))
