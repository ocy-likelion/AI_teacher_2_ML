from PIL import Image
import pytesseract
import io
from typing import BinaryIO

def ocr_image_to_text(image_file: BinaryIO) -> str:
    image = Image.open(image_file)
    
    text = pytesseract.image_to_string(image, lang='kor+eng+equ')
    return text.strip()

if __name__ == "__main__":
    import os
    sample_path = os.path.join("resources", "sample/M1_1_01_6915_3603.png")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            result = ocr_image_to_text(f)
            print("OCR 결과:\n", result)
    else:
        print(f"샘플 이미지가 존재하지 않습니다: {sample_path}")
