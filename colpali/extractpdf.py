import fitz  # PyMuPDF
from PIL import Image
import io
import os

def clear_directory(directory):
    """Remove all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # Remove the directory if empty
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def pdf_to_jpeg(pdf_path, output_folder):
    """Convert each page of a PDF to a JPEG image and save them in the output folder."""
    # Ensure the output directory exists and is empty
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        clear_directory(output_folder)
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    for page_number in range(num_pages):
        # Render page to an image
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        # Save the image as JPEG
        output_path = os.path.join(output_folder, f"page_{page_number + 1}.jpeg")
        img.save(output_path, "JPEG")
    # Close the PDF document
    pdf_document.close()

def main():
    # Path to your PDF file
    pdf_path = "<PDF path and filename>"
    # Get the directory where this script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Define the output folder as the "static" subfolder in the script's directory
    output_folder = os.path.join(script_directory, 'static')
    # Convert PDF to JPEG images
    pdf_to_jpeg(pdf_path, output_folder)

if __name__ == "__main__":
    main()
