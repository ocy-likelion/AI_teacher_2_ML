from openai import OpenAI
from config.config import config
import json
import re

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_ai_response(problem_text: str):
    prompt = config.PROMPT_TEMPLATE.format(problem_text=problem_text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational expert who returns structured JSON for math concepts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    content = response.choices[0].message.content

    match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
    if not match:
        raise ValueError("응답에서 JSON 블럭을 찾을 수 없습니다.")

    json_str = match.group(1)

    try:
        result = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 실패: {e}")

    # 필수 필드 체크
    if not all(key in result for key in ("summary", "explanation", "concept_tags")):
        raise ValueError("JSON에 필요한 필드가 없습니다.")

    return result


if __name__ == "__main__":
    sample_problem = (
        "가로의 길이가 210 m, 세로의 길이가 315 m인 직사각형 공터의 둘레에 "
        "일정한 간격으로 표지판을 세우려고 한다. 표지판 사이의 간격이 최대가 되도록 "
        "세울 때, 필요한 표지판은 몇 개인지 구하여라."
    )
    result = generate_ai_response(sample_problem)
    print("\n[RESULT] Summary:\n", result["summary"])
    print("\n[RESULT] Explanation:\n", result["explanation"])
    print("\n[RESULT] Concept Tags:\n", result["concept_tags"])
