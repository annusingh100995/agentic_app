from fastapi import FastAPI
from pydantic import BaseModel
from manager import run_agent_by_intent
from logger_config import logger

app = FastAPI()

class RequestBody(BaseModel):
    query: str

@app.post("/master")
async def master_api(body: RequestBody):
    logger.info(f"Received query: {body.query}")
    result = await run_agent_by_intent(body.query)
    logger.info(f"Master API returning result: {result}")
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",      # "file_name:app_instance"
        host="0.0.0.0",  # accessible from outside if needed
        port=8000,       # port number
        reload=True      # auto-reload on code changes (useful in development)
    )
