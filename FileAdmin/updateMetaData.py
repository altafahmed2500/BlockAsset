import datetime
import hashlib
from datetime import datetime
import json
import PyPDF2


def generate_file_hash(file_path, hash_algorithm='sha256'):
    # Create a hash object based on the specified algorithm
    hash_func = getattr(hashlib, hash_algorithm)()

    try:
        with open(file_path, 'rb') as file:
            # Read the file in chunks to avoid memory issues with large files
            while chunk := file.read(8192):  # 8 KB chunks
                hash_func.update(chunk)

        return hash_func.hexdigest()  # Return the hex digest of the hash
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


# Function to add custom metadata to a PDF file
def addCustomMetadataToPdf(input_pdf, output_pdf, metadata):
    # Open the existing PDF
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # Add all pages to the writer
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # Add custom metadata
        pdf_writer.add_metadata(metadata)

        # Write the updated PDF with metadata to a new file
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)

    print(f"Custom metadata added to {output_pdf}")


def updateMetaData(input_pdf, output_pdf, public_address):
    # Define custom metadata with current timestamp
    custom_metadata = {
        "/public_address": public_address,
        "/timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(custom_metadata)
    # Call the function with input and output files and custom metadata
    addCustomMetadataToPdf(input_pdf, output_pdf, custom_metadata)
    updated_hash = generate_file_hash(output_pdf, hash_algorithm='sha256')
    return updated_hash
    # print(updated_hash)
