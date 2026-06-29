# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-28 (Phase 4 agent runtime wrappers completed)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/phase4-real-agent-runtime-containers`

- Completed phases 1-3 and merged them to `main`.
- Started and completed Phase 4 — Real Agent Runtime Containers:
  - Converted Hermes and OpenClaw mock apps into HTTP wrappers that preserve `GET /health` and `POST /execute`.
  - Added simulator mode when no runtime command is configured.
  - Added runtime command mode via `AGENT_RUNTIME_COMMAND` and `AGENT_RUNTIME_TIMEOUT_SECONDS`.
  - Added structured timeout, missing-command, and non-zero-exit responses.
  - Added wrapper smoke tests covering simulator contracts, runtime success, and runtime failure.
  - Added runtime command env vars to `compose.yaml` and `.env.example`.
  - Replaced the example Cosmos emulator key in `.env.example` with a placeholder.
- Verification passed: agent wrapper tests `4 passed`; orchestrator tests `7 passed, 2 warnings`; `docker compose config --quiet` succeeded.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Commit and merge Phase 4 after final review.
2. Start Phase 5 on a new `clg/` branch: production orchestration behavior.
3. Convert keyword routing into configurable capability-based routing.
4. Add timeout/retry/partial-success behavior to agent clients.
5. Preserve the external `/tasks` and `/orchestrate` APIs while improving internals.

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
