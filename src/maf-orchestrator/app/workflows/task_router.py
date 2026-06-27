# Simple MAF Workflow for routing tasks to Hermes or OpenClaw
# Minimal working example using Microsoft Agent Framework (agent-framework)

import httpx
import os
from typing import Any

from agent_framework import Agent, tool

HERMES_ENDPOINT = os.getenv("HERMES_ENDPOINT", "http://localhost:8081")
OPENCLAW_ENDPOINT = os.getenv("OPENCLAW_ENDPOINT", "http://localhost:8082")

@tool
async def call_hermes(prompt: str) -> str:
    """Delegates complex or self-improving tasks to the Hermes agent."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{HERMES_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

@tool
async def call_openclaw(prompt: str) -> str:
    """Delegates personal/autonomous tasks to the OpenClaw agent."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{OPENCLAW_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

# MAF Agents
hermes_agent = Agent(
    name="Hermes",
    instructions="You are a self-improving autonomous agent. Use the call_hermes tool for analysis and complex tasks.",
    tools=[call_hermes]
)

openclaw_agent = Agent(
    name="OpenClaw",
    instructions="You are a reliable personal AI assistant. Use the call_openclaw tool for execution tasks.",
    tools=[call_openclaw]
)

async def run_simple_workflow(prompt: str) -> dict[str, Any]:
    """
    Minimal MAF-style workflow.
    In a full implementation this would use Workflow graph with planning/handoff.
    For Phase 1 we demonstrate tool calling + routing.
    """
    # Simple routing logic (will be replaced by real MAF Workflow later)
    use_hermes = any(kw in prompt.lower() for kw in ["analyze", "complex", "plan", "research"])
    
    results = []
    
    if use_hermes:
        result = await hermes_agent.run(prompt)
        results.append({"agent": "hermes", "output": result})
    
    # Always give OpenClaw a chance (or based on plan)
    result = await openclaw_agent.run(prompt)
    results.append({"agent": "openclaw", "output": result})
    
    return {
        "plan": "routed via MAF orchestrator",
        "results": results,
        "summary": "Task processed by selected agents using MAF tools."
    }
