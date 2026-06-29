# Proper MAF Workflow Graph: Planning → Conditional Handoff
# Uses Microsoft Agent Framework (agent-framework) for graph-based orchestration

import logging
import os
from typing import Any, Dict, Optional

from agent_framework import Agent, Workflow, tool

logger = logging.getLogger(__name__)

from app.state import state_store
from app.config import get_settings
from app.agents.hermes_client import HermesClient
from app.agents.openclaw_client import OpenClawClient

settings = get_settings()

# Real clients (point to deployed agents via env vars, or mocks in local compose)
hermes_client = HermesClient()
openclaw_client = OpenClawClient()

@tool
async def call_hermes(prompt: str) -> str:
    """MAF Tool: Delegates to the real (or mock) Hermes agent via HTTP."""
    response = await hermes_client.execute(prompt)
    return response.get("result", str(response))

@tool
async def call_openclaw(prompt: str) -> str:
    """MAF Tool: Delegates to the real (or mock) OpenClaw agent via HTTP."""
    response = await openclaw_client.execute(prompt)
    return response.get("result", str(response))

# MAF Agents would use tools, but for local demo we use direct clients in handoffs.
# TODO: full MAF Agent integration when client setup ready (e.g. from Foundry)
# hermes_agent = ...


# Planning step (can later be replaced by a Semantic Kernel / Azure OpenAI planner)
async def plan_task(input: str) -> Dict[str, Any]:
    """
    Planning node: analyzes the task and decides routing from ROUTE_CONFIG_JSON.
    Returns structured plan for conditional handoff.
    """
    decision = settings.route_config.resolve(input)

    plan = {
        "original_task": input,
        "reasoning": decision.reasoning,
        "route": decision.route,
        "agents": decision.agents,
        "capabilities": decision.capabilities,
        "steps": []
    }

    if "hermes" in decision.agents:
        plan["steps"].append("Hermes: Deep analysis, coding, review, and self-improvement")
    if "openclaw" in decision.agents:
        plan["steps"].append("OpenClaw: Execution and autonomous actions")

    logger.info("Planning complete. Route decision: %s agents=%s", decision.route, decision.agents)
    return plan

# Handoff / execution nodes - use real HTTP clients for demo
async def handoff_to_hermes(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Handoff node for Hermes - calls via HTTP client."""
    try:
        result = await hermes_client.execute(plan["original_task"])
        return {
            "agent": "hermes",
            "status": "success",
            "output": result,
            "plan": plan
        }
    except Exception as e:
        return {
            "agent": "hermes",
            "status": "failure",
            "error": str(e),
            "plan": plan
        }

async def handoff_to_openclaw(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Handoff node for OpenClaw - calls via HTTP client."""
    try:
        result = await openclaw_client.execute(plan["original_task"])
        return {
            "agent": "openclaw",
            "status": "success",
            "output": result,
            "plan": plan
        }
    except Exception as e:
        return {
            "agent": "openclaw",
            "status": "failure",
            "error": str(e),
            "plan": plan
        }

async def combine_results(hermes_result: Dict, openclaw_result: Dict) -> Dict[str, Any]:
    """Final combination step for parallel/sequential both case."""
    return {
        "final_status": "completed",
        "hermes": hermes_result,
        "openclaw": openclaw_result,
        "summary": "Task processed by multiple agents via MAF conditional handoff."
    }

async def run_pantheon_workflow(
    prompt: str, 
    checkpoint_id: Optional[str] = None
) -> dict[str, Any]:
    """
    Orchestrator using planning + conditional routing to agents via HTTP clients.
    Uses state store for checkpointing (Cosmos or in-memory fallback for local Docker).
    """
    # State / Resume
    if checkpoint_id:
        previous = await state_store.load_state(checkpoint_id)
        if previous and "plan" in previous:
            print(f"[Checkpoint] Resuming from {checkpoint_id}")
            plan = previous["plan"]
            results_so_far = previous.get("results", [])
        else:
            plan = await plan_task(prompt)
            results_so_far = []
    else:
        plan = await plan_task(prompt)
        results_so_far = []

    checkpoint_id = await state_store.save_state(
        checkpoint_id=checkpoint_id,
        task=prompt,
        plan=plan,
        results=results_so_far,
        status="planning_complete"
    )

    route = plan.get("route", "executor")
    agents = plan.get("agents") or (["hermes", "openclaw"] if route == "both" else [route])
    results = list(results_so_far)

    logger = logging.getLogger(__name__)

    if "hermes" in agents and not any(r.get("agent") == "hermes" for r in results):
        logger.info("Handoff to Hermes via client")
        hermes_out = await handoff_to_hermes(plan)
        results.append(hermes_out)
        await state_store.update_result(checkpoint_id, hermes_out)

    if "openclaw" in agents and not any(r.get("agent") == "openclaw" for r in results):
        logger.info("Handoff to OpenClaw via client")
        openclaw_out = await handoff_to_openclaw(plan)
        results.append(openclaw_out)
        await state_store.update_result(checkpoint_id, openclaw_out)

    if len(agents) > 1:
        hermes_r = next((r for r in results if r.get("agent") == "hermes"), {})
        openclaw_r = next((r for r in results if r.get("agent") == "openclaw"), {})
        execution = await combine_results(hermes_r, openclaw_r)
    else:
        execution = results[0] if results else {"status": "no_execution"}

    await state_store.save_state(
        checkpoint_id=checkpoint_id,
        task=prompt,
        plan=plan,
        results=results,
        status="completed"
    )

    return {
        "plan": plan,
        "execution": execution,
        "checkpoint_id": checkpoint_id,
        "summary": execution.get("summary", "Task completed via MAF orchestrator"),
        "agents_used": [r.get("agent") for r in results if isinstance(r, dict) and "agent" in r]
    }

