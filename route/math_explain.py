from flask import Blueprint, request, jsonify, current_app
from service.ocr_client import ocr_image_to_text
from service.openai_client import generate_ai_response

math_explain_bp = Blueprint('math_explain', __name__)

@math_explain_bp.route('/math-explain', methods=['POST'])
def math_explain():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']

    try:
        problem_text = ocr_image_to_text(image_file)
    except Exception as e:
        current_app.logger.error(f"OCR processing failed: {e}", exc_info=True)
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

    if not problem_text:
        return jsonify({'error': 'Failed to extract text from image'}), 500

    try:
        explanation_model = generate_ai_response(problem_text)
        result = explanation_model.model_dump()
        current_app.logger.info("AI response generated successfully.")
    except Exception as e:
        current_app.logger.error(f"AI processing failed: {e}", exc_info=True)
        return jsonify({'error': f'AI processing failed: {str(e)}'}), 500

    return jsonify(result)
