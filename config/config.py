import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EXPLANATION_PROMPT_TEMPLATE = os.getenv("EXPLANATION_PROMPT_TEMPLATE", "").replace("\\n", "\n")
    CONCEPT_PROMPT_TEMPLATE = os.getenv("CONCEPT_PROMPT_TEMPLATE", "").replace("\\n", "\n")

config = Config()
