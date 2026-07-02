# MAF Orchestrator entrypoint
# Uses Microsoft Agent Framework (MAF) for coordination of Hermes + OpenClaw agents
#
# SECURITY: Load all secrets from environment variables only.
# Never hardcode credentials. See docs/security-guidelines.md

import asyncio
import hashlib
import hmac
import json
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel, Field

import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from app.config import get_settings
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


def _verify_webhook_signature(body: bytes, signature: str | None) -> None:
    settings = get_settings()
    secret = settings.webhook_shared_secret
    if not secret:
        return

    if not signature or not signature.startswith("sha256="):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing webhook signature")

    expected = "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook signature")


def _event_type(payload: dict[str, Any], explicit_event: str | None) -> str:
    return explicit_event or str(
        payload.get("event")
        or payload.get("type")
        or payload.get("action")
        or payload.get("event_type")
        or "webhook.received"
    )


def _payload_prompt(source: str, event_type: str, payload: dict[str, Any]) -> str:
    """Build a bounded task prompt from the incoming webhook payload."""
    issue = payload.get("issue") if isinstance(payload.get("issue"), dict) else {}
    title = payload.get("title") or payload.get("message") or payload.get("summary") or issue.get("title")
    payload_excerpt = json.dumps(payload, default=str, ensure_ascii=False)[:4000]
    return (
        f"Webhook received from {source}.\n"
        f"Event type: {event_type}.\n"
        f"Title/message: {title or 'n/a'}\n\n"
        f"Payload excerpt:\n{payload_excerpt}\n\n"
        "Route this webhook to the appropriate agent and produce the next action."
    )

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


@app.post("/webhooks/{source}", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(
    source: str,
    request: Request,
    x_pantheon_event: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
    x_pantheon_signature_256: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
):
    """Receive an external webhook payload and route it through the orchestrator.

    If WEBHOOK_SHARED_SECRET is set, callers must sign the raw request body with
    HMAC-SHA256 and send either X-Pantheon-Signature-256 or GitHub's
    X-Hub-Signature-256 header as `sha256=<digest>`.
    """
    body = await request.body()
    signature = x_pantheon_signature_256 or x_hub_signature_256
    _verify_webhook_signature(body, signature)

    try:
        payload = json.loads(body.decode("utf-8")) if body else {}
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook payload must be JSON") from exc

    if not isinstance(payload, dict):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook payload must be a JSON object")

    event_type = _event_type(payload, x_pantheon_event or x_github_event)
    logger.info(
        "Received webhook: source=%s event_type=%s payload_bytes=%s",
        source,
        event_type,
        len(body),
    )

    result = await run_pantheon_workflow(
        prompt=_payload_prompt(source, event_type, payload),
        checkpoint_id=None,
    )

    return {
        "status": "accepted",
        "source": source,
        "event_type": event_type,
        "checkpoint_id": result.get("checkpoint_id"),
        "agents_used": result.get("agents_used", []),
        "summary": result.get("summary"),
    }
