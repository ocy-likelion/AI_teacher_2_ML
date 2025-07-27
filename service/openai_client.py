from openai import OpenAI
from config.config import config
import logging
from pydantic import BaseModel, ValidationError
from typing import List

client = OpenAI(api_key=config.OPENAI_API_KEY)

PROMPT_TEMPLATE = config.PROMPT_BASE + (
    " 반드시 JSON 형식으로만 응답해 주세요. "
    "{{"
    '"summary": "한 줄 요약", '
    '"explanation": "자세한 설명 (수식은 모두 $$ ... $$ 로 감쌉니다)", '
    '"concept_tags": ['
        '{{"name": "개념명1", "description": "간단한 설명1"}}, '
        '{{"name": "개념명2", "description": "간단한 설명2"}}, '
        '{{"name": "개념명3", "description": "간단한 설명3"}}, '
        '{{"name": "개념명4", "description": "간단한 설명4"}}'
    ']}} 문제: {problem_text}'
)

class ConceptTag(BaseModel):
    name: str
    description: str

class MathExplanation(BaseModel):
    summary: str
    explanation: str
    concept_tags: List[ConceptTag]


def generate_ai_response(problem_text: str) -> MathExplanation:
    user_prompt = PROMPT_TEMPLATE.format(problem_text=problem_text)

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an educational expert. You must output a JSON object. The object must have three keys: 'summary' (string), 'explanation' (string), and 'concept_tags' (an array of objects). Each object in the 'concept_tags' array must have two keys: 'name' (string) and 'description' (string). IMPORTANT: All strings in the JSON must be properly escaped. For example, any backslash `\\` character must be escaped as `\\\\`."},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    json_str = response.choices[0].message.content

    try:
        explanation_model = MathExplanation.model_validate_json(json_str)
    except ValidationError as e:
        logging.error(f"Pydantic validation failed for JSON: {json_str}")
        raise ValueError(f"JSON validation failed: {e}") from e
    return explanation_model


if __name__ == "__main__":
    sample_problem = (
        "가로의 길이가 210 m, 세로의 길이가 315 m인 직사각형 공터의 둘레에 "
        "일정한 간격으로 표지판을 세우려고 한다. 표지판 사이의 간격이 최대가 되도록 "
        "세울 때, 필요한 표지판은 몇 개인지 구하여라."
    )
    result = generate_ai_response(sample_problem)
    print("\n[RESULT] Summary:\n", result.summary)
    print("\n[RESULT] Explanation:\n", result.explanation)
    print("\n[RESULT] Concept Tags:\n", result.concept_tags)
