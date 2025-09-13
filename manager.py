from agents.agent_a import agent_a
from agents.agent_b import agent_b
from logger_config import logger

agents = {
    "agent_a": agent_a,
    "agent_b": agent_b
}

async def run_agent(agent_name: str, query: str):
    logger.info(f"Dispatching query to agent: {agent_name}")
    agent = agents.get(agent_name)
    if not agent:
        logger.error(f"Agent '{agent_name}' not found.")
        return f"Agent '{agent_name}' not found."

    try:
        result = await agent(query)
        logger.info(f"Agent '{agent_name}' returned result successfully.")
        return result
    except Exception as e:
        logger.exception(f"Error while running agent '{agent_name}': {str(e)}")
        return f"Error occurred in agent '{agent_name}'."
