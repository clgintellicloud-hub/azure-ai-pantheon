# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-28 (Phase 2 local orchestrator reliability completed)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/phase2-local-orchestrator-reliability`

- Completed Phase 1 and merged it to `main`.
- Started and completed Phase 2 — Local Orchestrator Reliability:
  - Updated FastAPI endpoint tests to use `httpx.ASGITransport`.
  - Added route-decision coverage for Hermes-only, OpenClaw-only, and both-agent prompts.
  - Added regression coverage to prevent raw prompt/secret logging.
  - Added safer orchestration request logging based on prompt length and checkpoint ID.
  - Added structured `HTTPException` mapping for unexpected workflow failures.
  - Replaced mutable Pydantic default metadata with `Field(default_factory=dict)`.
  - Preserved a top-level `result` field in `/orchestrate` responses for compatibility.
- Verified local orchestrator tests: `7 passed, 2 warnings`.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Commit and merge Phase 2 after final review.
2. Start Phase 3 on a new `clg/` branch: Azure agent endpoint wiring.
3. Output Hermes/OpenClaw FQDNs from Bicep.
4. Pass `HERMES_ENDPOINT` and `OPENCLAW_ENDPOINT` into the orchestrator Container App.
5. Add managed identity and required role assignments for Cosmos/Key Vault access.

## Current Open Questions / Risks
- How will MAF "talk to" existing Hermes/OpenClaw runtimes? (HTTP endpoints, MCP, A2A protocol, direct calls, etc.)
- Will we evolve the existing Docker + Bicep factories or create new ones specific to Pantheon?
- Scope: Is Pantheon only the orchestrator, or does it also include improved deployment for the agents themselves?
- Observability integration with Microsoft Foundry.

## Key Facts That Must Not Be Lost
- Project root is the root of this repository.
- GitHub user/org: clg-built4tech-azure
- Existing agent deployments use Node.js wrappers around `hermes-agent` CLI inside ACA containers.
- gh CLI is already authenticated with repo scope.
- Strong preference for filesystem-based context that survives reboots.

## Active Todos / Work Items
(See docs/TODOS.md or the live todo list in the current session)

---

**How to keep this file accurate:**
- This file gets updated (via search_replace or write) whenever major progress happens.
- It is deliberately short and scannable.
- Timestamp + summary of changes is added on every update.
