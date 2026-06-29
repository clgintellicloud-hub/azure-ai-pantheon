# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-28 (Azure orchestrator implementation phases started)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/phase1-azure-deploy-foundation`

- Documented the Azure orchestrator implementation phases in `docs/azure-orchestrator-implementation-phases.md`.
- Updated branching convention for this effort to `clg/` feature branches.
- Started Phase 1 — Azure Deploy Foundation:
  - Fixed reusable Container App env var rendering to use Bicep `items()`.
  - Added per-app `targetPort` support so the orchestrator can target port `8000` while agents keep `8080`.
  - Aligned Cosmos workflow state container to `workflow_state` with `/id` partition key.
  - Passed orchestrator Cosmos runtime config through Bicep.
- Verified `az bicep build --file infra/main.bicep` succeeds with warnings only.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Commit and merge Phase 1 after final review.
2. Start Phase 2 on a new `clg/` branch: local orchestrator reliability.
3. Fix `httpx` tests with `ASGITransport`.
4. Add structured orchestration errors and safer logging.
5. Add tests for Hermes-only, OpenClaw-only, both-agent routing, and checkpoint resume.

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
