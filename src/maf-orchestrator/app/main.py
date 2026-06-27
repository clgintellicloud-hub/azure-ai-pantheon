# MAF Orchestrator entrypoint
# Uses Microsoft Agent Framework (MAF) for coordination of Hermes + OpenClaw agents
#
# SECURITY: Load all secrets from environment variables only.
# Never hardcode credentials. See docs/security-guidelines.md

import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from app.workflows.task_router import run_simple_workflow

app = FastAPI(title="azure-ai-pantheon MAF Orchestrator")

class TaskRequest(BaseModel):
    prompt: str
    metadata: dict = {}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "framework": "microsoft-agent-framework",
        "version": "phase1-minimal"
    }

@app.post("/orchestrate")
async def orchestrate(request: TaskRequest):
    """Submit a task to the MAF orchestrator.
    
    Phase 1: Uses a minimal MAF workflow that routes to mock Hermes/OpenClaw agents.
    """
    result = await run_simple_workflow(request.prompt)
    
    return {
        "status": "processed",
        "input": request.prompt,
        "result": result
    }

@app.post("/tasks")
async def submit_task(request: TaskRequest):
    """Task submission endpoint (Phase 1 goal)."""
    response = await orchestrate(request)
    return {"task_id": "local-demo-001", **response}
