# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-27 (Routine context saving protocol fully active and documented)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
**Branch**: `grok/analyze-existing-factories`

- Performing initial analysis of the two existing agent deployment factories (azure-hermes-factory and oc-agent-main).
- Documenting common patterns, differences, and implications for the future MAF-based Pantheon orchestration layer.
- Created `docs/EXISTING_FACTORIES_ANALYSIS.md` as the first real artifact on this feature branch.

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
- Workspace: C:\Users\openclaw\Documents\grok
- GitHub user/org: clgintellicloud-hub
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
