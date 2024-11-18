from google.colab import files
uploaded = files.upload()

%pip install pdf2image pytesseract --quiet
!pip install pdf2image
!apt-get install poppler-utils
!pip install pytesseract
!pip install pandas
!pip install opencv-python
!sudo apt update
!sudo apt install -y tesseract-ocr
from pdf2image import convert_from_path
import cv2
import numpy as np
import pandas as pd  # Import Pandas for DataFrame operations
# Import the pytesseract module
import pytesseract
# Set Tesseract path for Colab
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

import pytesseract
from pdf2image import convert_from_path

# convert to image using resolution 600 dpi
pages = convert_from_path("/content/sv600_g_fine.pdf", 600)

# extract text
text_data = ''
for page in pages:
    text = pytesseract.image_to_string(page)
    text_data += text + '\n'
print(text_data)
