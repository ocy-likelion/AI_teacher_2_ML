from flask import Blueprint, request, jsonify
from service.ocr_client import ocr_image_to_text
from service.openai_client import generate_ai_response
import traceback

math_explain_bp = Blueprint('math_explain', __name__)

@math_explain_bp.route('/math-explain', methods=['POST'])
def math_explain():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']

    try:
        problem_text = ocr_image_to_text(image_file)
    except Exception as e:
        print("OCR 처리 에러:", e)
        traceback.print_exc()
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

    if not problem_text:
        return jsonify({'error': 'Failed to extract text from image'}), 500

    try:
        result = generate_ai_response(problem_text)
        print("AI 응답 결과:", result)
    except Exception as e:
        print("AI 처리 에러:", e)
        traceback.print_exc()
        return jsonify({'error': f'AI processing failed: {str(e)}'}), 500

    return jsonify(result)
