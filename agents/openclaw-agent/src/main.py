# Mock OpenClaw Agent for local development
# Simulates the real OpenClaw agent (personal AI assistant style)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mock OpenClaw Agent")

class TaskRequest(BaseModel):
    prompt: str
    context: dict = {}

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "openclaw-mock"}

@app.post("/execute")
async def execute(request: TaskRequest):
    # Simulate autonomous personal agent
    response = {
        "agent": "openclaw",
        "result": f"OpenClaw executed task: {request.prompt} [autonomous actions taken]",
        "actions": ["query", "decide", "act"],
        "status": "completed"
    }
    return response
