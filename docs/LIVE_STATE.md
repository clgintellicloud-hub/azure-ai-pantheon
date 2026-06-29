# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-29 (Phase 5 Dapr production orchestration implemented)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/phase5-production-dapr-orchestration`

- Completed phases 1-4 and merged them to `main`.
- Started and completed Phase 5 — Production Dapr Orchestration:
  - Added `docs/production-ai-agent-orchestrator.md` in the requested architecture/output format.
  - Added Dapr-aware orchestrator config: Dapr sidecar port, Dapr app IDs, state store, pub/sub, and configurable route JSON.
  - Added capability-based routing via `RouteConfig` with researcher/coder/executor/reviewer/both routes.
  - Added `DaprAgentClient` with Dapr service invocation and direct HTTP fallback.
  - Updated Hermes/OpenClaw clients to use Dapr service invocation when `DAPR_HTTP_PORT` is set.
  - Added Azure OpenAI, Azure Service Bus, and Dapr component Bicep modules.
  - Enabled Dapr on orchestrator and agent Container Apps.
  - Added base specialized Python agent template under `agents/templates/python-agent`.
  - Added tests for configurable routes and Dapr invocation URL generation.
- Verification passed: orchestrator tests `9 passed, 2 warnings`; agent wrapper tests `4 passed`; `az bicep build --file infra/main.bicep` succeeded with warnings only; `docker compose config --quiet` succeeded.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Commit and merge Phase 5 after final review.
2. Start Phase 6 on a new `clg/` branch: observability and operations.
3. Wire OpenTelemetry export to Azure Monitor/Application Insights.
4. Add `/health/deep` checks for Cosmos, Dapr, Hermes, OpenClaw, and Azure OpenAI config.
5. Add deployment smoke tests and runbooks.

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
