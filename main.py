from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from manager import run_agent_by_intent
from logger_config import logger
from auth import verify_api_key
import uvicorn

app = FastAPI()

class RequestBody(BaseModel):
    query: str

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/master")
async def master_api(body: RequestBody, x_api_key : str = Depends(verify_api_key)):
    logger.info(f"Received query: {body.query}")
    result = await run_agent_by_intent(body.query)
    logger.info(f"Master API returning result: {result}")
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
