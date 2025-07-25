from PIL import Image, UnidentifiedImageError
import cv2
import pytesseract
import io
import numpy as np

def preprocess(pil_image):
    img = np.array(pil_image.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = cv2.resize(img, (512, 512))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binarized = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return Image.fromarray(binarized)

def ocr_image_to_text(image_file):
    image_bytes = image_file.read()
    pil_image = Image.open(io.BytesIO(image_bytes))
    image = preprocess(pil_image)

    text = pytesseract.image_to_string(image, lang='kor+eng+equ')
    image_file.seek(0)
    return text.strip()

if __name__ == "__main__":
    import os
    sample_path = os.path.join("resources", "M1_1_01_6915_3603.png")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            result = ocr_image_to_text(f)
            print("OCR 결과:\n", result)
    else:
        print(f"샘플 이미지가 존재하지 않습니다: {sample_path}")
