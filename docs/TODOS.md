# TODOS.md — Persistent Task List for azure-ai-pantheon

This file holds the project's task list in a way that survives reboots. 
It can be updated by the agent (via tools) or the user.

Use simple markdown checkboxes. Move completed items to a "Done" section or delete them.

## Current / Active (grok/next-steps-orchestrator branch)
- [x] Create branch grok/next-steps-orchestrator
- [x] Create minimal working mock Hermes + OpenClaw agents (for local compose)
- [x] Update compose.yaml for hot reload
- [x] Flesh out src/maf-orchestrator/ into a working FastAPI + MAF app (planning + routing workflow)
- [x] Add MAF dependency + minimal working example (Agent + simple workflow using tools)
- [x] Implement basic task submission endpoint (POST /tasks)
- [x] Add health check + basic logging + OpenTelemetry setup (console)
- [x] Review and improve Bicep (added acr, aca-env, cosmos, key-vault modules)
- [ ] Flesh out remaining Bicep modules (monitoring, foundry, etc.)
- [ ] Wire real integration points to Hermes and OpenClaw (start with HTTP)
- [x] Add Cosmos DB for state in orchestrator code (with MAF checkpointing + resume)
- [ ] Upgrade GitHub Actions workflows to use OIDC properly
- [ ] Decide on primary language for MAF (Python strongly recommended)

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
