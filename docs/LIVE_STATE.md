# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-27 (Routine context saving protocol fully active and documented)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `grok/azure-maf-architecture`

- Implementing the full recommended Azure architecture for MAF-based orchestration of Hermes + OpenClaw agents.
- Added `docs/architecture.md` (core services table, high-level architecture, detailed GitHub repo file structure).
- Scaffolded production-ready project layout:
  - `infra/` with Bicep (main + reusable modules)
  - `src/maf-orchestrator/` (FastAPI + MAF skeleton)
  - `agents/` placeholders
  - `compose.yaml`, `azd.yaml`
  - GitHub Actions workflow stubs for controllable deploys
- Updated README.md and AGENTS.md to make the architecture the guiding reference.
- Builds directly on `docs/EXISTING_FACTORIES_ANALYSIS.md`.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo + set up context & branching infrastructure.
- 2026-06-27: Created first real feature branch: `grok/analyze-existing-factories`
- Created initial analysis document: `docs/EXISTING_FACTORIES_ANALYSIS.md` covering the two prior factories and Pantheon implications.
- Updated LIVE_STATE and SESSION_LOG as part of the routine context process.

## Next Immediate Steps
1. Continue deep dive on this branch: Bicep modules, GitHub Actions workflows, agent variants.
2. Identify concrete extension points for MAF orchestration (HTTP, health, config).
3. Research current MAF patterns for multi-agent orchestration and ACA deployment.
4. Propose high-level architecture for the Pantheon conductor (in a follow-up document or PR).
5. (Routine) Use save-context discipline after progress.

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
