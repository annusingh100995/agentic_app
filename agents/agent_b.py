# agents/agent_b.py
import os
from dotenv import load_dotenv
import httpx
from langgraph.graph import StateGraph
from pydantic import BaseModel
from logger_config import logger
import asyncio

# Load env variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# LangGraph state
class AgentState(BaseModel):
    query: str
    result: str = ""

async def agent_b(query: str):
    logger.info(f"Agent B processing query: {query}")
    async def weather_node(state: AgentState):
        city = state.query.strip()
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

        if "current" in data:
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            summary = (
                f"Weather in {city}: {condition}, "
                f"temperature {temp_c}°C, humidity {humidity}%, wind {wind_kph} kph."
            )
        else:
            summary = f"Could not fetch weather for '{city}'. Please check the city name."
        logger.info(f"Agent B result: {summary}")
        return {"result": summary}

    workflow = StateGraph(AgentState)
    workflow.add_node("weather", weather_node)
    workflow.set_entry_point("weather")
    workflow.set_finish_point("weather")

    app = workflow.compile()
    output = await app.ainvoke({"query": query})
    return output["result"]
