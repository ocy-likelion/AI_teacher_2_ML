from openai import OpenAI
from config.config import config
import json
import re

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_explanation_and_concepts(problem_text):
    explanation_prompt = config.EXPLANATION_PROMPT_TEMPLATE.format(problem_text=problem_text)
    explanation_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly math tutor who explains problems in simple Korean."},
            {"role": "user", "content": explanation_prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    explanation = explanation_response.choices[0].message.content.strip()
    
    concept_prompt = config.CONCEPT_PROMPT_TEMPLATE.format(problem_text=problem_text)
    concept_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational expert who returns structured JSON for math concepts."},
            {"role": "user", "content": concept_prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    concept_raw = concept_response.choices[0].message.content.strip()
    
    try:
        json_block = re.search(r"\[.*\]", concept_raw, re.DOTALL)
        concept_tags = json.loads(json_block.group()) if json_block else []
    except Exception as e:
        print("JSON 파싱 오류:", e)
        concept_tags = []

    return {
        "explanation": explanation,
        "concept_tags": concept_tags
    }


if __name__ == "__main__":
    sample_problem = "가로의 길이가 210 m, 세로의 길이가 315 m인 직사각형 공터의 둘레에 일정한 간격으로 표지판을 세우려고 한다. 표지판 사이의 간격이 최대가 되도록 세울 때, 필요한 표지판은 몇 개인지 구하여라."
    result = generate_explanation_and_concepts(sample_problem)
    print("Explanation:\n", result["explanation"])
    print("\nConcept Tags:\n", result["concept_tags"])
