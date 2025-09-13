from fastapi import FastAPI, Request
from manager import run_agent
from logger_config import logger
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

class RequestBody(BaseModel):
    agent: str
    query: str

# Instrument FastAPI endpoints
Instrumentator().instrument(app).expose(app)  # exposes /metrics


# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/master")
async def master_api(body: RequestBody):
    logger.info(f"Received master API request: agent={body.agent}, query={body.query}")
    result = await run_agent(body.agent, body.query)
    logger.info(f"Master API returning result: {result}")
    return {"agent": body.agent, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
