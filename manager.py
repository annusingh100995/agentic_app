# manager.py
from agents.agent_a import agent_a
from agents.agent_b import agent_b

agents = {
    "agent_a": agent_a,
    "agent_b": agent_b
}

async def run_agent(agent_name: str, query: str):
    agent = agents.get(agent_name)
    if not agent:
        return f"Agent '{agent_name}' not found."
    return await agent(query)
