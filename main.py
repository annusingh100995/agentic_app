# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from manager import run_agent
import uvicorn

app = FastAPI()

class RequestBody(BaseModel):
    agent: str
    query: str

@app.post("/master")
async def master_api(body: RequestBody):
    result = await run_agent(body.agent, body.query)
    return {"agent": body.agent, "result": result}

# Run with: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
