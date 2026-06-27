# Architecture & Design Decisions

Record important decisions here so future sessions understand the "why".

## 2026-06-27 — Initial Setup
- Created `AGENTS.md`, enhanced README, `docs/` structure, and `scripts/resume-context.ps1` specifically to survive computer reboots and new Grok sessions.
- Decision: Put durable project context **inside the repo** using standard files rather than relying only on chat history or global ~/.grok state.

## (Add future decisions below)
- Language choice for MAF layer (Python / .NET)
- How Hermes/OpenClaw will be invoked from MAF (HTTP, MCP, A2A, sidecar, etc.)
- Whether to evolve the existing Bicep or create new Pantheon-specific IaC
- Observability strategy (direct to Foundry vs custom)
