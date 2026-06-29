# Azure Orchestrator Implementation Phases

## Goal

Implement the Azure-hosted Pantheon orchestrator that manages Hermes AI Agents and OpenClaw AI Agents running as Azure Container Apps. The orchestrator should expose a stable task API, route work to the appropriate agent containers, persist workflow checkpoints, and emit operational telemetry.

## Branching and Merge Policy

- All feature branches for this effort start with `clg/`.
- Each phase is implemented on its own `clg/<phase-name>` branch.
- When a phase is complete:
  1. Run verification commands.
  2. Commit the phase.
  3. Push the feature branch.
  4. Merge back to `main`.
  5. Pull `main` before starting the next phase.

## Phase 1 — Azure Deploy Foundation

**Objective:** Make the current Azure infrastructure and app configuration internally consistent enough to deploy.

**Scope:**
- Fix Bicep compile blockers.
- Make the reusable Container App module support different target ports.
- Align Cosmos DB database/container/partition-key settings between Bicep and the Python state store.
- Pass the orchestrator's non-secret runtime config through Bicep.
- Keep real secrets out of source and rely on environment variables or Managed Identity.

**Key files:**
- `infra/main.bicep`
- `infra/modules/container-app.bicep`
- `infra/modules/cosmos-db.bicep`
- `src/maf-orchestrator/app/config.py`
- `src/maf-orchestrator/app/state/cosmos_state_store.py`

**Done when:**
- `az bicep build --file infra/main.bicep` succeeds.
- The orchestrator Container App targets port `8000`.
- Hermes/OpenClaw agent apps continue to target port `8080`.
- Cosmos state docs can use checkpoint IDs as both item IDs and partition keys.

## Phase 2 — Local Orchestrator Reliability

**Objective:** Make the local Python orchestrator reliable before deploying it to Azure.

**Scope:**
- Fix tests for current `httpx` using `ASGITransport`.
- Add route tests for Hermes-only, OpenClaw-only, and both-agent flows.
- Add checkpoint save/resume tests.
- Add structured error handling around orchestration requests.
- Stop logging raw prompt content.

**Key files:**
- `src/maf-orchestrator/tests/test_orchestrator.py`
- `src/maf-orchestrator/app/main.py`
- `src/maf-orchestrator/app/workflows/task_router.py`
- `src/maf-orchestrator/app/state/cosmos_state_store.py`

**Done when:**
- Local orchestrator tests pass.
- `/health`, `/tasks`, and `/orchestrate` have stable behavior.
- Agent call failures return structured responses instead of unhandled exceptions.

## Phase 3 — Azure Agent Endpoint Wiring

**Objective:** Deploy an orchestrator that can call ACA-hosted Hermes and OpenClaw endpoints.

**Scope:**
- Output Hermes/OpenClaw FQDNs from Bicep.
- Pass `HERMES_ENDPOINT` and `OPENCLAW_ENDPOINT` into the orchestrator Container App.
- Add managed identity support to Container Apps.
- Add role assignments required for Cosmos/Key Vault access.
- Deploy mock agent containers first to validate cloud wiring.

**Key files:**
- `infra/main.bicep`
- `infra/modules/container-app.bicep`
- `infra/modules/key-vault.bicep`
- `infra/modules/cosmos-db.bicep`
- `agents/hermes-agent/*`
- `agents/openclaw-agent/*`

**Done when:**
- ACA-hosted orchestrator can call ACA-hosted Hermes and OpenClaw services.
- `/orchestrate` succeeds against cloud endpoints.
- The orchestrator does not use `localhost` for cloud agent calls.

## Phase 4 — Real Agent Runtime Containers

**Objective:** Replace mock Hermes/OpenClaw containers with real agent wrapper containers.

**Scope:**
- Preserve a stable HTTP contract for the orchestrator: `GET /health` and `POST /execute`.
- Wrap the real Hermes/OpenClaw agent runtimes inside container entrypoints.
- Return agent name, version, status, and result metadata from each agent.
- Add smoke tests for each real agent container.

**Key files:**
- `agents/hermes-agent/Dockerfile`
- `agents/hermes-agent/src/*`
- `agents/openclaw-agent/Dockerfile`
- `agents/openclaw-agent/src/*`
- `docs/EXISTING_FACTORIES_ANALYSIS.md`
- `docs/KNOWN_PRIOR_WORK.md`

**Done when:**
- The orchestrator can call real Hermes/OpenClaw wrappers through the same `/execute` contract used by mocks.
- Each real agent has a working `/health` endpoint in ACA.

## Phase 5 — Production Orchestration Behavior

**Objective:** Move from demo routing to production-grade orchestration behavior.

**Scope:**
- Convert keyword routing into configurable capability-based routing.
- Replace custom async flow with real MAF workflow graph nodes where appropriate.
- Add timeouts, retries, partial-success behavior, and circuit-breaker rules.
- Preserve the external `/tasks` and `/orchestrate` APIs.

**Key files:**
- `src/maf-orchestrator/app/workflows/task_router.py`
- `src/maf-orchestrator/app/agents/hermes_client.py`
- `src/maf-orchestrator/app/agents/openclaw_client.py`
- `src/maf-orchestrator/app/models.py`

**Done when:**
- Routes can be changed without editing core orchestration code.
- A failed agent call produces a predictable status.
- Multi-agent workflows can return partial success when only one agent fails.

## Phase 6 — Observability and Operations

**Objective:** Make the system observable and operable in Azure.

**Scope:**
- Wire OpenTelemetry to Azure Monitor/Application Insights and Foundry where available.
- Add safe span metadata: checkpoint ID, route, agents used, status, and duration.
- Add `/health/deep` for Cosmos, Hermes, OpenClaw, and configured endpoints.
- Add deployment smoke tests and runbooks.

**Key files:**
- `src/maf-orchestrator/app/main.py`
- `src/maf-orchestrator/app/middleware/logging.py`
- `docs/runbooks/*`
- `.github/workflows/*`

**Done when:**
- Operators can see orchestrator and agent-call traces.
- Deployment smoke tests verify health, single-agent routes, both-agent route, and checkpoint resume.
- Runbooks document rollback and incident triage.

## Phase 7 — CI/CD and Mainline Hygiene

**Objective:** Automate validation and deployments while keeping `main` stable.

**Scope:**
- Add or update CI for Python tests and Bicep build validation.
- Add separate deployment workflows for infra, orchestrator, Hermes, and OpenClaw.
- Use GitHub OIDC for Azure login.
- Add path filters so unrelated changes do not deploy every component.

**Key files:**
- `.github/workflows/ci.yml`
- `.github/workflows/deploy-iac.yml`
- `.github/workflows/deploy-orchestrator.yml`
- `.github/workflows/deploy-hermes.yml`
- `.github/workflows/deploy-openclaw.yml`
- `docs/security-guidelines.md`

**Done when:**
- PR validation runs without manual steps.
- Azure deployments use OIDC, not committed credentials.
- Component-specific changes trigger only the needed deployment workflow.

## Current Phase

Work has started on **Phase 1 — Azure Deploy Foundation** on branch `clg/phase1-azure-deploy-foundation`.
