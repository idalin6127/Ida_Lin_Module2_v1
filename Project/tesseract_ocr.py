from PIL import Image
import pytesseract #pip install pytesseract first

# Load an image using Pillow (PIL)
image = Image.open('processed.png')

# Perform OCR on the image
text = pytesseract.image_to_string(image, lang='eng')

print("The identification results are as follows: ")
print(text)
