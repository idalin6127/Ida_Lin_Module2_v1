import cv2
from PIL import Image
import pytesseract

# ===== Step 1: Image Preprocessing =====
input_image = 'Food_Description.jpg'           # Original image filename
processed_image = 'processed_food_description_multi.png'   # Filename for the preprocessed image

# Read the image
img = cv2.imread(input_image)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply binary thresholding (you can adjust the threshold value based on image quality)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Save the preprocessed image
cv2.imwrite(processed_image, thresh)
print(f"Image preprocessing completed. Saved as {processed_image}")

# ===== Step 2: OCR Recognition =====
# Open the preprocessed image
image = Image.open(processed_image)

# Test several PSM modes
for psm in [3, 6, 7, 11]:
    print(f"\n--- OCR Result with PSM {psm} ---")
    text = pytesseract.image_to_string(image, lang='spa', config=f'--psm {psm}')
    print(text)

    # ===== Optional: Save the result to a text file =====
    with open(f"output_food_descpription_psm{psm}.txt", "w", encoding="utf-8") as f:
        f.write(text)

print("\nText recognition completed. Result saved to output.txt")
