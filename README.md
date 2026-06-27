# azure-ai-pantheon

**AI Agent orchestration**

This project builds the management, coordination, and orchestration layer for running and composing **Hermes Agent** and **OpenClaw** agents on **Azure Container Apps**, with heavy use of **Microsoft Agent Framework (MAF)**.

## Quick Start for Humans and Agents

```powershell
cd <project-root>
```

**For AI agents (especially after reboot)**: Read `AGENTS.md` first — it contains full project context, related code locations, and resume instructions.

## Goals
- Provide a "Pantheon" conductor for multiple heterogeneous autonomous agents.
- Leverage Microsoft Agent Framework for workflows, routing, state, and observability.
- Evolve and unify existing deployment patterns for Hermes and OpenClaw on ACA.

## Recommended Architecture
See the full production-grade recommendation:
- **[docs/architecture.md](docs/architecture.md)** — Azure services (ACA + Microsoft Foundry + Cosmos DB + ACR + Managed Identity), high-level architecture, and GitHub repo structure for controllable IaC + app deployments.

Key stack:
- MAF orchestrator in Azure Container Apps
- Hermes + OpenClaw agents in isolated ACA instances
- Cosmos DB for durable MAF workflow state/checkpointing
- Microsoft Foundry for models, tools, and rich observability

## Documentation
- **[AGENTS.md](AGENTS.md)** — Essential reading for any AI coding agent. Contains project history, related code, architecture notes, and recovery instructions.
- `docs/architecture.md` — Target Azure architecture and file structure.
- `docs/security-guidelines.md` — GitHub repo & GitHub Actions security rules (no secrets, OIDC, etc.).
- `SECURITY.md` — Security policy.
- `docs/local-development.md` — How to set up local secrets safely (always use .env.example).
- `docs/` — Detailed architecture, decisions, status, runbooks, and existing factories analysis.

## Current Status
See `AGENTS.md` and files in `docs/`.

**Phase 1 in progress** (on `grok/next-steps-orchestrator`):
- Minimal MAF orchestrator + workflow running locally via `docker compose up`
- Mock Hermes & OpenClaw agents for development
- See docs/local-development.md for how to test.

## Related Work
This repo is the orchestration layer on top of earlier infrastructure work in the related `azure-hermes-factory` and `oc-agent-main` projects (sibling repositories with prior Bicep IaC and agent container definitions). 

See `docs/EXISTING_FACTORIES_ANALYSIS.md` and `docs/KNOWN_PRIOR_WORK.md` for analysis of those patterns.

## Contributing / Working With Agents
- Always keep `AGENTS.md` and supporting docs up to date so future sessions (after reboots) do not lose context.
- **All feature branches must be prefixed with `grok/`** (e.g. `grok/add-maf-orchestrator`). See [AGENTS.md](AGENTS.md) → Branching Strategy.
- Use the helper: `.\scripts\create-grok-branch.ps1 your-feature-name` or the `git grok-branch` alias (after setup).
- **Security first**: Follow `docs/security-guidelines.md` and `SECURITY.md`. Never commit secrets. Use OIDC for Azure. See `.gitignore` for required patterns.

## Branching
See the full rules in [AGENTS.md](AGENTS.md). Main stays `main`. Everything else uses the `grok/` prefix.

## License
TBD
