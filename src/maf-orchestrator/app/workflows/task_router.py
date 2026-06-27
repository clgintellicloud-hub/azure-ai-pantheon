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
    MAF-style orchestrator workflow for Phase 1.
    1. Planning step (simple rule-based for now, can be replaced by LLM planner)
    2. Route to appropriate agent(s) using MAF Agents + tools
    """
    # --- Planning step ---
    # In full MAF this would be an LLM-powered planner agent.
    # For now, use simple heuristics to demonstrate workflow.
    prompt_lower = prompt.lower()
    use_hermes = any(kw in prompt_lower for kw in ["analyze", "complex", "plan", "research", "strategy"])
    use_openclaw = True  # OpenClaw is general purpose

    plan = {
        "task": prompt,
        "steps": [],
        "agents_to_use": []
    }

    if use_hermes:
        plan["steps"].append("Use Hermes for deep analysis/self-improvement")
        plan["agents_to_use"].append("hermes")
    if use_openclaw:
        plan["steps"].append("Use OpenClaw for execution/personal actions")
        plan["agents_to_use"].append("openclaw")

    # --- Execution step using MAF Agents ---
    results = []

    if use_hermes:
        hermes_result = await hermes_agent.run(prompt)
        results.append({"agent": "hermes", "output": hermes_result})

    if use_openclaw:
        openclaw_result = await openclaw_agent.run(prompt)
        results.append({"agent": "openclaw", "output": openclaw_result})

    return {
        "plan": plan,
        "results": results,
        "summary": "Task decomposed and routed using MAF workflow + tools."
    }
