import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PROMPT_TEMPLATE = os.getenv("PROMPT_TEMPLATE", "").replace("\\n", "\n")

config = Config()
