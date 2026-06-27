# MAF Orchestrator entrypoint
# Uses Microsoft Agent Framework (MAF) for coordination of Hermes + OpenClaw agents
#
# SECURITY: Load all secrets from environment variables only.
# Never hardcode credentials. See docs/security-guidelines.md

import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from app.workflows.task_router import run_pantheon_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("maf-orchestrator")

# Basic OpenTelemetry setup (Phase 1 - console for local, later export to App Insights)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

tracer = trace.get_tracer(__name__)

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
    
    Uses a proper MAF Workflow Graph:
    - Planning step
    - Conditional handoff to HermesAgent / OpenClawAgent / Both
    - Basic success/failure handling
    """
    with tracer.start_as_current_span("orchestrate_task"):
        logger.info(f"Received task: {request.prompt[:100]}...")
        
        result = await run_pantheon_workflow(request.prompt)
        
        # Extract agents from different result shapes
        agents = []
        if "execution" in result:
            if isinstance(result["execution"], dict) and "hermes" in result["execution"]:
                agents = ["hermes", "openclaw"]
            elif "agent" in result.get("execution", {}):
                agents = [result["execution"]["agent"]]
        logger.info(f"Workflow completed for task. Agents used: {agents}")
        
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
