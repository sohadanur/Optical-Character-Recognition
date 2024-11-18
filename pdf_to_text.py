from google.colab import files
uploaded = files.upload()
!pip install pdf2image
!apt-get install poppler-utils
!pip install pytesseract
!pip install pandas
!pip install opencv-python
!sudo apt update
!sudo apt install -y tesseract-ocr
# Set Tesseract path for Colab
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
import pandas as pd  # Import Pandas for DataFrame operations


# Function to extract text using Tesseract OCR
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to process each page
def process_page(page):
    try:
        # Convert page image to numpy array
        page_arr = np.array(page)
        # Convert to grayscale
        page_arr_gray = cv2.cvtColor(page_arr, cv2.COLOR_BGR2GRAY)

        # Extract data using Tesseract
        d = pytesseract.image_to_data(page_arr_gray, output_type=pytesseract.Output.DICT)
        d_df = pd.DataFrame.from_dict(d)
        # Identify block numbers for header and footer
        block_num = int(d_df.loc[d_df['level'] == 2, 'block_num'].max())
        header_index = d_df[d_df['block_num'] == 1].index.values
        footer_index = d_df[d_df['block_num'] == block_num].index.values
        # Combine text excluding header and footer
        text = ' '.join(
            d_df.loc[
                (d_df['level'] == 5) & (~d_df.index.isin(header_index) & ~d_df.index.isin(footer_index)),
                'text'
            ].values
        )
        return text
    except Exception as e:
        # Handle exceptions
        return str(e)

# Main code to process PDF
print("PDF converted to images successfully!")
pdf_file = r"/content/宮崎日大slc手書きコピー.pdf" #Path of the file you uploaded in collab
pages = convert_from_path(pdf_file)

# List to store extracted text and confidence values
extracted_data = []

for page in pages:
    text = process_page(page)
    extracted_data.append({ "Text": text })

# Print the extracted data
for page_number, data in enumerate(extracted_data, start=1):
    print(f"Page {page_number}\nText: {data['Text']}\n")
