# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-29 (Webhook payload ingress implemented)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `clg/add-webhook-payload-ingress`

- Added a PR-based feature branch for webhook payload ingress.
- Implemented `POST /webhooks/{source}` on the MAF orchestrator:
  - Accepts JSON payloads from external systems.
  - Derives event type from `X-Pantheon-Event`, `X-GitHub-Event`, or payload fields.
  - Optionally validates HMAC-SHA256 signatures with `WEBHOOK_SHARED_SECRET`.
  - Supports `X-Pantheon-Signature-256` and GitHub-compatible `X-Hub-Signature-256` headers.
  - Converts the payload into an orchestration task and returns `202 Accepted` with checkpoint/agent summary.
- Updated `.env.example`, `compose.yaml`, `docs/local-development.md`, and `docs/production-ai-agent-orchestrator.md` with webhook usage and security notes.
- Verification passed: orchestrator tests `12 passed, 2 warnings`; agent wrapper tests `4 passed`; `az bicep build --file infra/main.bicep` succeeded with warnings only; `docker compose config --quiet` succeeded.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Create and merge the GitHub PR for `clg/add-webhook-payload-ingress`.
2. Start Phase 6 on a new `clg/` branch: observability and operations.
3. Wire OpenTelemetry export to Azure Monitor/Application Insights.
4. Add `/health/deep` checks for Cosmos, Dapr, Hermes, OpenClaw, webhook config, and Azure OpenAI config.
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
