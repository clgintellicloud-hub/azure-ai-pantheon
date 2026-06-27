# Known Prior Work

This document captures external codebases that form the foundation for azure-ai-pantheon.

## 1. Azure Hermes Factory

**Purpose**: Production-ready Bicep IaC + container definitions for running Hermes AI Agents on Azure Container Apps.

**Note**: Full source resides in the related sibling repository `azure-hermes-factory`. See `docs/EXISTING_FACTORIES_ANALYSIS.md` for detailed analysis.

**Key Components**:
- `infra/bicep/` — Subscription-scoped deployment
  - Resource groups (dev + prod)
  - ACR (`ocrocagentdev`)
  - Log Analytics
  - ACA Environments
  - Container Apps (named agents + dynamic `hermes-ai-N` count)
- `agents/`
  - `hermes/`, `analyst/`, `openclaw/` variants
  - `Dockerfile` (Node 22 base)
  - `src/agent.js` — Thin HTTP wrapper that spawns the real `hermes-agent gateway run ...`
  - `config/hermes.json`
- Scripts for build, revisions, rollback, smoke tests

**Patterns to Preserve or Improve**:
- Managed identity + ACR
- Dev/Prod separation
- ACA revisions for versioning
- Simple health endpoints
- Wrapper approach to run the official Hermes CLI inside containers

## 2. OC Agent Main

Similar structure to Azure Hermes Factory, with more emphasis on OpenClaw configuration (`openclaw.json`).

**Note**: Full source resides in the related sibling repository `oc-agent-main`. See `docs/EXISTING_FACTORIES_ANALYSIS.md` for detailed analysis.

## Why This Matters for Pantheon
The Pantheon (this repo) should not re-invent the container deployment wheel. Instead it should:
- Consume or extend the deployment artifacts from these factories.
- Provide the intelligence layer (MAF-based) on top.
- Offer unified control, routing, and observability across Hermes and OpenClaw instances.

When resuming work, always review `docs/EXISTING_FACTORIES_ANALYSIS.md` and `docs/KNOWN_PRIOR_WORK.md` (which summarize patterns from these external projects).
