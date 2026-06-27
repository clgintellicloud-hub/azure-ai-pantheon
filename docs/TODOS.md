# TODOS.md — Persistent Task List for azure-ai-pantheon

This file holds the project's task list in a way that survives reboots. 
It can be updated by the agent (via tools) or the user.

Use simple markdown checkboxes. Move completed items to a "Done" section or delete them.

## Current / Active
- [x] Deep-dive into existing `azure-hermes-factory` Bicep and Docker code (see docs/EXISTING_FACTORIES_ANALYSIS.md)
- [x] Research and adopt recommended Azure MAF architecture (docs/architecture.md)
- [x] Scaffold full project structure + Bicep + MAF stubs (on branch `grok/azure-maf-architecture`)
- [ ] Flesh out remaining Bicep modules (cosmos-db, key-vault, monitoring, foundry)
- [ ] Implement initial MAF orchestrator workflows that call Hermes/OpenClaw (as tools or HTTP)
- [ ] Add full OpenTelemetry + Foundry tracing to orchestrator
- [ ] Decide on primary language for MAF (Python strongly recommended)
- [ ] Create more agent-specific container stubs or link to existing factories
- [ ] Add complete GitHub Actions (ci, deploy-all, reusable workflows)

## Backlog
- Improve container wrappers for better health, observability, and MCP exposure
- Add unified control plane features (scaling, versioning via ACA revisions)
- Integrate telemetry with Microsoft Foundry
- Create deployment templates specific to the Pantheon layer

## Done
- [x] 2026-06-27: Set up robust reboot-safe context system (AGENTS.md + LIVE_STATE.md + save scripts + git discipline)
- [x] 2026-06-27: Branching convention enforcement (`grok/` prefix + helper)
- [x] 2026-06-27: Initial factories analysis + full recommended MAF architecture scaffolding

## Notes
- For short-term in-session tasks, the `todo_write` tool can be used, then persisted here at save time.
- Keep this list reasonably short and actionable.
