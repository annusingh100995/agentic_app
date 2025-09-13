from agents.agent_a import agent_a
from agents.agent_b import agent_b
from logger_config import logger
from intent_classifier import classify_intent

agents = {
    "summarize": agent_a,
    "weather": agent_b
}

async def run_agent_by_intent(query: str):
    intent = await classify_intent(query)
    logger.info(f"Detected intent: {intent}")

    agent = agents.get(intent)
    if not agent:
        logger.warning(f"No agent available for intent '{intent}'")
        return f"Sorry, I can't handle this request."

    logger.info(f"Dispatching query to agent: {intent}")
    result = await agent(query)
    return result
