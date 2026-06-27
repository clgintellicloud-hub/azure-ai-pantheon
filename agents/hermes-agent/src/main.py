# Mock Hermes Agent for local development
# Simulates the real Hermes agent behavior

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mock Hermes Agent")

class TaskRequest(BaseModel):
    prompt: str
    context: dict = {}

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "hermes-mock"}

@app.post("/execute")
async def execute(request: TaskRequest):
    # Simulate self-improving agent behavior
    response = {
        "agent": "hermes",
        "result": f"Hermes processed: {request.prompt} [with skills and memory]",
        "plan": ["analyze", "act", "learn"],
        "confidence": 0.92
    }
    return response
