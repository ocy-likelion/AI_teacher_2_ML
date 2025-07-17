from PIL import Image
import pytesseract
import io

def ocr_image_to_text(image_file):
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
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
