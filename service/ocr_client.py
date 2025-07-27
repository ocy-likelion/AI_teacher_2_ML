from PIL import Image
import pytesseract
from typing import BinaryIO
import gc

MAX_IMAGE_DIMENSION = 2000

def ocr_image_to_text(image_file: BinaryIO) -> str:
    text_result = ""
    try:
        with Image.open(image_file) as image:
            image = image.convert('L')

            if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
                image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)

            tesseract_config = r'--dpi 300'
            text_result = pytesseract.image_to_string(image, lang='kor+eng+equ', config=tesseract_config)
    finally:
        gc.collect()
    return text_result.strip()

if __name__ == "__main__":
    import os
    sample_path = os.path.join("resources", "sample/M1_1_01_6915_3603.png")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            result = ocr_image_to_text(f)
            print("OCR 결과:\n", result)
    else:
        print(f"샘플 이미지가 존재하지 않습니다: {sample_path}")
