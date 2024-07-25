# from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask import *
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF
from pdf_processing_scripts.extract_text import extract_text_func
from pdf_processing_scripts.extract_images import extract_images_func
from pdf_processing_scripts.extract_tables import extract_tables_func
from pdf_processing_scripts.count_pages import count_pages_func
from pdf_processing_scripts.pdftoimage import pdf_img_func
import csv


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part"
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.pdf'):
        # Remove any existing file in the uploads directory
        for existing_file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Rename the new uploaded file to input.pdf
        filename = "input.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the selected options
        options = request.form.to_dict()
        return process_options(filepath, options)
    
    return "Invalid file type"

def process_options(filepath, options):
    if 'extract_text' in options:
        # Execute extract text function
        text = extract_text_func(filepath)
        return redirect(url_for('text_result'))

    if 'extract_images' in options:
        # Execute extract images function
        extract_images_func(filepath)
        return redirect(url_for('images_result'))

    if 'extract_tables' in options:
        # Execute extract tables function
        extract_tables_func(filepath)
        return redirect(url_for('tables_result'))
    
    if 'count_pages' in options:
        # Execute count pages function
        pages = count_pages_func(filepath)
        return redirect(url_for('pages_result'))
    
    if 'pdftoimage' in options:
        pdf_img_func(filepath)
        return redirect(url_for('pdf_img_result'))

    return "No valid options selected"

filename = "input.pdf"
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/text')
def text_result():
    text = extract_text_func(filepath)
    return render_template('text.html', app = text)

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)

# Route to display the images
@app.route('/images')
def images_result():
    images_dir = 'images'
    images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    return render_template('images.html', images=images)

# Route to generate and download the PDF
@app.route('/download_images_pdf')
def download_images_pdf():
    images_dir = 'images'
    images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for image in images:
        image_path = os.path.join(images_dir, image)
        pdf.add_page()
        pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

    pdf_output = 'extracted_images.pdf'
    pdf.output(pdf_output)

    return send_file(pdf_output, as_attachment=True)


# @app.route('/tables')
# def tables_result():
#     directory = 'extracted_tables'
#     if not os.path.exists(directory):
#         return []
#     csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
#     json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
#     return render_template('tables.html', csv_files = csv_files, json_files = json_files)
#     # return render_template('tables.html', app = files)

# @app.route('/download/<path:filename>')
# def download(filename):
#     directory = 'extracted_tables'
#     return send_from_directory(directory, filename, as_attachment=True)

@app.route('/tables')
def tables_result():
    directory = 'extracted_tables'
    if not os.path.exists(directory):
        return render_template('tables.html', csv_files=[], json_files=[], csv_contents={})
    
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Read CSV contents
    csv_contents = {}
    for file in csv_files:
        with open(os.path.join(directory, file), newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_contents[file] = [row for row in reader]

    return render_template('tables.html', 
                           csv_files=csv_files, 
                           json_files=json_files, 
                           csv_contents=csv_contents)

@app.route('/download/<path:filename>')
def download(filename):
    directory = 'extracted_tables'
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/pages')
def pages_result():
    pages = count_pages_func(filepath)
    return render_template('pages.html', app = pages)

# Route to serve individual PDF images
@app.route('/pdftoimage/<filename>')
def send_pdf_image(filename):
    return send_from_directory('pdf_imgs', filename)

# Route to display all PDF images
@app.route('/pdftoimage')
def pdf_img_result():
    img_dir = 'pdf_imgs'
    images = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    return render_template('pdf_img.html', images=images)

# Route to download individual images
@app.route('/download_img_pdf/<filename>')
def download_img_pdf(filename):
    return send_from_directory('pdf_imgs', filename, as_attachment=True)

# # Route to generate and download each PDF image separately
# @app.route('/download_img_pdf/<filename>')
# def download_img_pdf(filename):
#     image_path = os.path.join('pdf_imgs', filename)

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

#     pdf_output = f'pdf_image_{filename}.pdf' 
#     pdf.output(pdf_output)

#     return send_file(pdf_output, as_attachment=True)

# # Route to generate and download the PDF of all images
# @app.route('/download_img_pdf')
# def download_img_pdf():
#     img_dir = 'pdf_imgs'
#     images = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     for image in images:
#         image_path = os.path.join(img_dir, image)
#         pdf.add_page()
#         pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

#     pdf_output = 'pdf_images.pdf'
#     pdf.output(pdf_output)

#     return send_file(pdf_output, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)