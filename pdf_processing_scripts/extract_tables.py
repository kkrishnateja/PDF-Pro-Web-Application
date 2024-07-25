import pdfplumber
import os
import pandas as pd

def extract_tables_func(filepath, output_format = ['csv', 'json']):
    # output_format = ['csv', 'json']
    # Specify the output directory
    output_dir = 'extracted_tables'
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Remove existing files in the output directory
    for existing_file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, existing_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Open the PDF file
    with pdfplumber.open(filepath) as pdf:
        csv_count = 0
        json_count = 0
        # Iterate through each page
        for page_number, page in enumerate(pdf.pages):
            # Extract tables from the page
            tables = page.extract_tables()

            # Save each table in the specified format
            for table in tables:
                df = pd.DataFrame(table)
                csv_count += 1
                output_path = os.path.join(output_dir, f'table_{csv_count}.{output_format[0]}')
                if output_format[0] == 'csv':
                    df.to_csv(output_path, index=False)
                # elif output_format == 'json':
                #     df.to_json(output_path, orient='records')
                else:
                    print(f"Unsupported format: {output_format[0]}")

            # Save each table in the specified format
            for table in tables:
                df = pd.DataFrame(table)
                json_count += 1
                output_path = os.path.join(output_dir, f'table_{json_count}.{output_format[1]}')
                # if output_format == 'csv':
                #     df.to_csv(output_path, index=False)
                if output_format[1] == 'json':
                    df.to_json(output_path, orient='records')
                else:
                    print(f"Unsupported format: {output_format[1]}")

        print(f"Tables extracted and saved in {output_format} format successfully!")


# Example usage
# extract_tables_func('pdf_images.pdf')
# extract_tables_func('sample.pdf')