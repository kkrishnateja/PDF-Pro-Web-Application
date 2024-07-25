import fitz  # PyMuPDF
import io
import os
from PIL import Image

def extract_images_func(filepath):
    # Directory to save images
    images_dir = 'images'
    
    # Remove existing images in the directory if it exists
    if os.path.exists(images_dir):
        for filename in os.listdir(images_dir):
            file_path = os.path.join(images_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        # Create the directory if it doesn't exist
        os.makedirs(images_dir)

    # Open the PDF file
    pdf_file = fitz.open(filepath)

    # Iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # Get the page itself
        page = pdf_file.load_page(page_index)
        # Get the list of images on the page
        image_list = page.get_images(full=True)
        # Print the number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print(f"[!] No images found on page {page_index}")

        for image_index, img in enumerate(image_list, start=1):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # Get the image extension
            image_ext = base_image["ext"]
            # Load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # Save it to the images directory
            image.save(open(os.path.join(images_dir, f"image{page_index+1}_{image_index}.{image_ext}"), "wb"))

    print("Images extracted successfully!")


# Example usage
# extract_images_func('sample.pdf')
