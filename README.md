# azure-ai-pantheon

**AI Agent orchestration**

This project builds the management, coordination, and orchestration layer for running and composing **Hermes Agent** and **OpenClaw** agents on **Azure Container Apps**, with heavy use of **Microsoft Agent Framework (MAF)**.

## Quick Start for Humans and Agents

```powershell
cd "C:\Users\openclaw\Documents\grok"
```

**For AI agents (especially after reboot)**: Read `AGENTS.md` first — it contains full project context, related code locations, and resume instructions.

## Goals
- Provide a "Pantheon" conductor for multiple heterogeneous autonomous agents.
- Leverage Microsoft Agent Framework for workflows, routing, state, and observability.
- Evolve and unify existing deployment patterns for Hermes and OpenClaw on ACA.

## Documentation
- **[AGENTS.md](AGENTS.md)** — Essential reading for any AI coding agent. Contains project history, related code, architecture notes, and recovery instructions.
- `docs/` — Detailed architecture, decisions, status, and runbooks (to be expanded).

## Current Status
See `AGENTS.md` and files in `docs/`.

## Related Work
This repo is the orchestration layer on top of earlier infrastructure work:
- `../claude-code/azure-hermes-factory/`
- `../../Downloads/oc-agent-main/oc-agent-main/`

## Contributing / Working With Agents
Always keep `AGENTS.md` and supporting docs up to date so future sessions (after reboots) do not lose context.

## License
TBD
