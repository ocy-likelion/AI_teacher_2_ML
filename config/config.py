import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PROMPT_BASE = os.getenv("PROMPT_BASE")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

config = Config()
