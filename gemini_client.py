from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL")

# Initialize Gemini client via OpenAI-compatible API
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
