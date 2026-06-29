# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-28 (Phase 3 Azure agent endpoint wiring completed)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/phase3-azure-agent-endpoint-wiring`

- Completed Phase 1 and Phase 2 and merged both to `main`.
- Started and completed Phase 3 — Azure Agent Endpoint Wiring:
  - Added system-assigned managed identity to Container Apps.
  - Passed ACA-hosted `HERMES_ENDPOINT` and `OPENCLAW_ENDPOINT` into the orchestrator app.
  - Added Hermes/OpenClaw FQDN outputs from `infra/main.bicep`.
  - Added `infra/modules/orchestrator-access.bicep` for orchestrator access grants.
  - Granted the orchestrator managed identity Cosmos DB SQL Built-in Data Contributor access.
  - Granted the orchestrator managed identity Key Vault Secrets User access.
  - Cleaned up Key Vault RBAC Bicep syntax and added module outputs needed by access wiring.
- Verified `az bicep build --file infra/main.bicep` succeeds with warnings only.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Commit and merge Phase 3 after final review.
2. Start Phase 4 on a new `clg/` branch: real Hermes/OpenClaw runtime containers.
3. Preserve the stable agent wrapper contract: `GET /health` and `POST /execute`.
4. Replace mock agent implementations with wrappers around the real runtimes.
5. Add smoke tests for each real agent container.

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
