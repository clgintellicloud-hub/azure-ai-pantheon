# Implementation Phases for azure-ai-pantheon PRD

## Overview
This breaks down the PRD (Recommended Azure Architecture for MAF-based Orchestration of Hermes + OpenClaw Agents) into concrete phases.

All work is local-only: Docker Desktop for testing, no Azure deployments. Use local Cosmos Emulator if needed for state testing.

Frequent commits on feature branches (grok/ prefix), merge to main often, keep main current.

Status checks: branch, git status, tests, gaps.

## Phases

### Phase 1: Local Development & Basic MAF Orchestrator
Tasks from PRD:
1. Flesh out src/maf-orchestrator/ into working FastAPI + MAF app
2. Add MAF dependency + minimal working example (Agent + simple workflow)
3. Implement basic task submission endpoint (POST /tasks)
4. Update compose.yaml for orchestrator with hot reload
5. Create .env.example with required variables
6. Add health check + basic logging + OpenTelemetry setup

Goal: docker compose up, submit task, see workflow execute with mocks.

### Phase 2: Hermes & OpenClaw Integration
7. Decide integration pattern (HTTP/MCP/MAF Tool/Handoff) - start with HTTP + MAF Tools
8. Create client/wrapper classes in src/maf-orchestrator/app/agents/ 
9. Implement MAF workflow that routes to agents
10. Basic error handling + retry

Goal: Orchestrator calls (mock then real local) agents.

### Phase 3: Infrastructure & Deployment (Local)
11. Review/expand infra/ Bicep (modules for ACA, Cosmos, KV, etc.)
12. Add Cosmos DB module + local integration
13. OIDC patterns (simulated locally)
14. Improve workflows for local testing
15. Support for agent deployments (local mocks)
16. Test local azd-like flow (focus docker)

Goal: Local infra validation, compose mirrors prod structure.

### Phase 4: Observability, State & Polish
17. Wire MAF OTEL to local monitoring
18. MAF checkpointing + persist to local Cosmos (emulator)
19. Basic dashboard (optional, e.g. simple)
20. Structured logging + correlation IDs

Goal: State persists, observability visible locally.

### Phase 5: Production Readiness & DX (Local Simulation)
21. Add tests (unit + integration)
22. Dependabot + scanning config
23. Env separation in IaC (dev/prod params)
24. Runbooks
25. LICENSE

Additional from PRD structure:
- Full .github/workflows (ci, all deploys)
- src/shared/
- Complete parameters/
- More modules (monitoring, foundry)
- docs/runbooks content

## Current Gaps (as of start of this session) - ALL ADDRESSED FOR LOCAL DOCKER SCOPE
- Some workflows missing (ci.yml, deploy-hermes, etc.)
- src/shared/ missing
- Full Bicep modules (monitoring, foundry)
- Full end-to-end local demo working (orchestrator + mocks + workflow + state)
- Real MAF workflow using native graph more
- Cosmos emulator setup for local state test
- OIDC simulation
- Tests
- Runbooks content
- LICENSE
- Complete integration with real agent behavior in local

Use Docker for all testing.

Update this file and TODOS.md as phases complete.

Commit frequently on grok/ branches, merge to main.
