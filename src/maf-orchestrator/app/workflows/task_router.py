# Proper MAF Workflow Graph: Planning → Conditional Handoff
# Uses Microsoft Agent Framework (agent-framework) for graph-based orchestration

import httpx
import os
from typing import Any, Dict, Optional

from agent_framework import Agent, Workflow, tool

from app.state import state_store
from app.config import get_settings

settings = get_settings()

HERMES_ENDPOINT = os.getenv("HERMES_ENDPOINT", "http://localhost:8081")
OPENCLAW_ENDPOINT = os.getenv("OPENCLAW_ENDPOINT", "http://localhost:8082")

@tool
async def call_hermes(prompt: str) -> str:
    """Tool for delegating to Hermes (self-improving / analysis agent)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{HERMES_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

@tool
async def call_openclaw(prompt: str) -> str:
    """Tool for delegating to OpenClaw (personal / execution agent)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{OPENCLAW_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

# Define MAF Agents
hermes_agent = Agent(
    name="HermesAgent",
    instructions="You are a self-improving autonomous agent specialized in analysis, planning, and learning. Use tools when appropriate.",
    tools=[call_hermes]
)

openclaw_agent = Agent(
    name="OpenClawAgent",
    instructions="You are a reliable personal AI assistant focused on execution and autonomous actions. Use tools when appropriate.",
    tools=[call_openclaw]
)

# Planning step (can later be replaced by a full Planner Agent using LLM)
async def plan_task(input: str) -> Dict[str, Any]:
    """
    Planning node: Analyzes the task and decides routing.
    Returns structured plan for conditional handoff.
    """
    prompt_lower = input.lower()
    
    use_hermes = any(kw in prompt_lower for kw in ["analyze", "complex", "plan", "research", "strategy", "deep"])
    use_openclaw = True  # Default to include OpenClaw unless purely analytical
    
    # For "both" cases
    if use_hermes and "and" in prompt_lower or "also" in prompt_lower:
        route = "both"
    elif use_hermes:
        route = "hermes"
    else:
        route = "openclaw"
    
    plan = {
        "original_task": input,
        "reasoning": f"Detected keywords leading to route={route}",
        "route": route,
        "steps": []
    }
    
    if route in ["hermes", "both"]:
        plan["steps"].append("Hermes: Deep analysis and self-improvement")
    if route in ["openclaw", "both"]:
        plan["steps"].append("OpenClaw: Execution and autonomous actions")
    
    return plan

# Handoff / execution nodes
async def handoff_to_hermes(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Handoff node for Hermes."""
    try:
        result = await hermes_agent.run(plan["original_task"])
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
    """Handoff node for OpenClaw."""
    try:
        result = await openclaw_agent.run(plan["original_task"])
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

async def create_pantheon_workflow() -> Workflow:
    """
    Builds a proper MAF Workflow Graph:
    
    input -> plan_task 
           -> conditional handoff:
               - hermes
               - openclaw
               - both (sequential for now)
           -> success/failure handling
    """
    wf = Workflow(name="PantheonTaskOrchestrator")
    
    # Add nodes
    wf.add_node("plan", plan_task)
    wf.add_node("hermes", handoff_to_hermes)
    wf.add_node("openclaw", handoff_to_openclaw)
    wf.add_node("combine", combine_results)
    
    # Main flow
    wf.add_edge("plan", "hermes", condition=lambda plan: plan.get("route") in ["hermes", "both"])
    wf.add_edge("plan", "openclaw", condition=lambda plan: plan.get("route") in ["openclaw", "both"])
    
    # For "both" case, combine results after both complete
    wf.add_edge("hermes", "combine", condition=lambda r: r.get("plan", {}).get("route") == "both")
    wf.add_edge("openclaw", "combine", condition=lambda r: r.get("plan", {}).get("route") == "both")
    
    # Simple success path for single agent cases (we can improve with a finalizer later)
    # For demo, the last node result is returned
    
    return wf

# Convenience function for FastAPI with MAF checkpointing support
async def run_pantheon_workflow(
    prompt: str, 
    checkpoint_id: Optional[str] = None
) -> dict[str, Any]:
    """
    Entry point that runs the full MAF workflow graph with state persistence.

    - If checkpoint_id is provided, attempts to resume from previous state.
    - Saves state after planning and after each agent handoff (MAF checkpointing).
    - Returns the final result + checkpoint_id for future resumption.
    """
    # Try to resume from checkpoint
    previous_state = None
    if checkpoint_id:
        previous_state = await state_store.load_state(checkpoint_id)
        if previous_state:
            print(f"[Checkpoint] Resuming from {checkpoint_id}")
            # For simplicity in Phase 2, we can return saved state or re-execute missing parts.
            # Here we re-execute but use saved plan if available.
            if "plan" in previous_state:
                plan = previous_state["plan"]
            else:
                plan = await plan_task(prompt)
        else:
            print(f"[Checkpoint] Checkpoint {checkpoint_id} not found, starting fresh.")
            plan = await plan_task(prompt)
    else:
        plan = await plan_task(prompt)

    # Save initial state after planning
    checkpoint_id = await state_store.save_state(
        checkpoint_id=checkpoint_id,
        task=prompt,
        plan=plan,
        results=[],
        status="in_progress"
    )

    route = plan.get("route")
    results = previous_state.get("results", []) if previous_state else []

    if route in ["hermes", "both"] and not any(r.get("agent") == "hermes" for r in results):
        hermes_out = await handoff_to_hermes(plan)
        results.append(hermes_out)
        await state_store.update_result(checkpoint_id, hermes_out)

    if route in ["openclaw", "both"] and not any(r.get("agent") == "openclaw" for r in results):
        openclaw_out = await handoff_to_openclaw(plan)
        results.append(openclaw_out)
        await state_store.update_result(checkpoint_id, openclaw_out)

    final_result: Dict[str, Any]
    if route == "both":
        # For "both" we may need to combine
        hermes_r = next((r for r in results if r.get("agent") == "hermes"), {})
        openclaw_r = next((r for r in results if r.get("agent") == "openclaw"), {})
        combined = await combine_results(hermes_r, openclaw_r)
        final_result = {
            "plan": plan,
            "execution": combined,
            "workflow": "MAF graph with conditional handoff + checkpointing"
        }
    else:
        final_result = {
            "plan": plan,
            "execution": results[0] if results else {},
            "workflow": "MAF graph with conditional handoff + checkpointing"
        }

    # Final save
    await state_store.save_state(
        checkpoint_id=checkpoint_id,
        task=prompt,
        plan=plan,
        results=results,
        status="completed"
    )

    final_result["checkpoint_id"] = checkpoint_id
    return final_result

