from PIL import Image
import pytesseract

# Optional: Path to tesseract executable (only needed on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Load the .tif image
image = Image.open('C:\\AI_Coop\\Homework\\Week2\\Project\\my_handwriting_train\\my_handwriting_sample.tif')  # Replace with your .tif file path

# OCR the image
text = pytesseract.image_to_string(image, lang='chi_sim')  # Use 'your_lang' if using custom model

# Output the recognized text
print(text)

