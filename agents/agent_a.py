# agents/agent_a.py
import os
from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from logger_config import logger
import asyncio


# Load env variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client via OpenAI-compatible API
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL = "gemini-2.0-flash"

SYSTEM_MESSAGE = "You are an assistant that summarizes text in a concise and clear way."

def user_prompt_for(text: str):
    prompt = (
        "Summarize the following text in one short sentence, keeping it clear and concise.\n\n"
        f"{text}"
    )
    return prompt

# Define LangGraph state
class AgentState(BaseModel):
    query: str
    result: str = ""

async def agent_a(query: str):
    logger.info(f"Agent A processing query: {query}")
    await asyncio.sleep(1)  # simulate work
    async def summarize_node(state: AgentState):
        response = gemini_via_openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_prompt_for(state.query)}
            ]
        )
        # Gemini output is usually in response.choices[0].message.content
        summary = response.choices[0].message.content
        logger.info(f"Agent A result: {summary}")
        return {"result": summary}

    workflow = StateGraph(AgentState)
    workflow.add_node("summarizer", summarize_node)
    workflow.set_entry_point("summarizer")
    workflow.set_finish_point("summarizer")

    app = workflow.compile()
    output = await app.ainvoke({"query": query})
    return output["result"]
