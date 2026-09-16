import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")


def validate_config():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from the .env file.")

    if not POSTGRES_URL:
        raise ValueError("POSTGRES_URL is missing from the .env file.")