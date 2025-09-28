from fastapi import APIRouter
from pydantic import BaseModel
from gemini_client import gemini_via_openai_client, MODEL
from logger_config import logger

router = APIRouter()

# Request/Response models
class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str

SYSTEM_MESSAGE = "You are an assistant that summarizes text in a concise and clear way."
def user_prompt_for(text: str):
    prompt = (
        "Summarize the following text in one short sentence, keeping it clear and concise.\n\n"
        f"{text}"
    )
    return prompt

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_agent(body: SummaryRequest):
    logger.info(f"Agent A processing query: {body.text}")

    response = gemini_via_openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_prompt_for(body.text)}
            ]
        )
        # Gemini output is usually in response.choices[0].message.content
    summary = response.choices[0].message.content
    logger.info(f"Agent A result: {summary}")
    
    # Example: naive first 50 chars
    return SummaryResponse(summary=summary)
