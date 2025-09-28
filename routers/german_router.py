from fastapi import APIRouter
from gemini_client import gemini_via_openai_client, MODEL  # your Gemini client
from pydantic import BaseModel
import json
from logger_config import logger

router = APIRouter()

# Define request and response models
class GrammarRequest(BaseModel):
    sentence: str

class GrammarResponse(BaseModel):
    base_sentence: str
    prediction: str
    modal_present: str
    modal_past: str
    simple_past: str
    subjunctive_true: str
    subjunctive_wuerde: str
    perfect: str
    perfect_subjunctive: str
    subordinate_wenn: str
    subordinate_ob: str
    subordinate_dass: str
    wishful: str
    reported: str

@router.post("/grammar", response_model=GrammarResponse)
async def grammar_agent(body: GrammarRequest):
    logger.info(f"Agent A processing query: {body.sentence}")
    system_message = """
    You are a German grammar assistant. 
    Given a base sentence, generate transformations in different grammatical forms:
    - Prediction (future)
    - Modal verbs (present & past)
    - Simple past
    - Subjunctive (true & würde)
    - Perfect tense
    - Perfect subjunctive
    - Subordinate clauses (wenn, ob, dass)
    - Wishful thinking
    - Reported speech
    Return output as JSON with the exact keys:
    base_sentence, prediction, modal_present, modal_past, simple_past,
    subjunctive_true, subjunctive_wuerde, perfect, perfect_subjunctive,
    subordinate_wenn, subordinate_ob, subordinate_dass, wishful, reported
    """

    user_prompt = f"Base sentence: {body.sentence}\nGenerate all forms in JSON."

    # Call Gemini API
    response = gemini_via_openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    # Parse the JSON output from Gemini
    try:
        result_json = json.loads(response.choices[0].message.content)
    except Exception:
        result_json = {"base_sentence": body.sentence}  # fallback in case of error

    return result_json
