# MAF Orchestrator entrypoint
# Uses Microsoft Agent Framework (MAF) for coordination of Hermes + OpenClaw agents
#
# SECURITY: Load all secrets from environment variables only.
# Never hardcode credentials. See docs/security-guidelines.md

import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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
    metadata: dict = Field(default_factory=dict)
    checkpoint_id: str | None = None  # For resuming MAF workflow state from Cosmos

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
    - Cosmos DB checkpointing for durable state (if configured)
    """
    with tracer.start_as_current_span("orchestrate_task"):
        logger.info(
            "Received task request: prompt_length=%s checkpoint=%s",
            len(request.prompt),
            request.checkpoint_id,
        )
        
        try:
            result = await run_pantheon_workflow(
                prompt=request.prompt,
                checkpoint_id=request.checkpoint_id
            )
        except Exception as exc:
            logger.exception("Workflow execution failed")
            raise HTTPException(
                status_code=502,
                detail="Workflow execution failed"
            ) from exc
        
        # Extract agents from different result shapes
        agents = []
        exec_data = result.get("execution", {})
        if isinstance(exec_data, dict) and "hermes" in exec_data:
            agents = ["hermes", "openclaw"]
        elif "agent" in exec_data:
            agents = [exec_data["agent"]]
        
        logger.info(f"Workflow completed for task. Agents used: {agents}")
        
        return {
            "status": "processed",
            "input": request.prompt,
            "checkpoint_id": result.get("checkpoint_id"),
            "agents_used": result.get("agents_used", []),
            "result": result,
            "plan": result.get("plan"),
            "summary": result.get("summary"),
            "details": result.get("execution")
        }

@app.post("/tasks")
async def submit_task(request: TaskRequest):
    """Task submission endpoint (supports resume via checkpoint_id)."""
    response = await orchestrate(request)
    return {"task_id": response.get("checkpoint_id", "local-demo-001"), **response}
