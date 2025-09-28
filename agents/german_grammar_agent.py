from dotenv import load_dotenv
import os
from openai import OpenAI
from logger_config import logger

# Load env variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL")

# Initialize Gemini client via OpenAI-compatible API
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


async def grammar_agent(query: str) -> dict:
    logger.info(f"Agent A processing query: {query}")
    system_message = """
    You are a German grammar assistant. 
    Given a base sentence, generate transformations in different grammatical forms:
    - Prediction
    - Modal verbs (present & past)
    - Simple past
    - Subjunctive (true & würde)
    - Perfect tense
    - Perfect subjunctive
    - Subordinate clauses (wenn, ob, dass)
    - Wishful thinking
    - Reported speech
    Return output as JSON.

    For example:
    Base sentence Ich trinke einen Kaffee 
    Prediction (future) Ich werde einen Kaffee trinken 
    Modal Verb (present) Ich will einen Kaffee trinken 
    Modal Verb (Past) Ich wollte einen Kaffee trinken 
    Simple Past Ich trank einen Kaffee 
    Subjunctive (true & würde) Ich tränke einen Kaffee / Ich würde einen Kaffee trinken 
    Perfect Tense Ich habe einen Kaffee getrunken 
    Past Tense Subjunctive Ich hätte einen Kaffee getrunken 
    Subordinate Clauses (wenn) Ich kriege Kopfweh, wenn ich einen Kaffee trinke 
    Subordinate Clauses (ob) Ich weiß nicht, ob ich einen Kaffee trinken soll / will 
    Subordinate Clauses (dass) Ich hoffe, dass ich einen Kaffee trinken kann 
    Wishful Thinking (Konj. II) Ich wünschte, dass ich einen Kaffee trinken könnte Ich wünschte, ich könnte einen Kaffee trinken 
    Reported Speech (Konj. I) Es heißt, er trinke einen Kaffee Er hat gesagt, er trinke einen Kaffee
    """
    
    user_prompt = f"Base sentence: {query}\nGenerate all forms."
    
    response = gemini_via_openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content
