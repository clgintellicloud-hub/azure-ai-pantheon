# Production AI Agent Orchestrator on Azure Container Apps

## 1. Architecture Overview

Recommended pattern: a dedicated Orchestrator Container App coordinates specialized custom agents and managed Azure AI Agent Service agents. Azure Container Apps hosts all custom containers with Dapr enabled. Dapr provides service invocation, pub/sub fan-out, and a state-store abstraction backed by Azure Cosmos DB.

Diagram description:

```text
Client / API / Scheduler
        |
        v
+-------------------------------+
| ACA: maf-orchestrator         |
| FastAPI + workflow router     |
| Dapr app id: orchestrator     |
+---------------+---------------+
                |
                | Dapr service invocation / pubsub
                v
+---------------+---------------+       +-------------------------------+
| ACA: researcher-agent         |       | Azure AI Agent Service         |
| ACA: coder-agent              | <---> | managed agents/tools           |
| ACA: executor-agent           |       +-------------------------------+
| ACA: reviewer-agent           |
+---------------+---------------+
                |
                v
+-------------------------------+
| Dapr components               |
| state: Cosmos DB              |
| pubsub: Azure Service Bus     |
+---------------+---------------+
                |
                v
+-------------------------------+
| Azure OpenAI / Key Vault /    |
| App Insights / Log Analytics  |
+-------------------------------+
```

Component interaction flow:

1. A client posts a task to `/tasks` or `/orchestrate` on the orchestrator.
2. The orchestrator creates or resumes a checkpoint in Cosmos DB.
3. The router maps the task to a capability route: `researcher`, `coder`, `executor`, `reviewer`, `hermes`, `openclaw`, or `both`.
4. The orchestrator invokes the selected custom agent through Dapr service invocation or calls a managed Azure AI Agent Service agent through an adapter.
5. Agents call tools/function handlers and may publish events through Dapr pub/sub.
6. Short-term workflow state, checkpoints, and long-term memory are persisted in Cosmos DB.
7. All components emit structured logs and OpenTelemetry traces to Application Insights/Log Analytics.

## 2. Technology Stack Recommendation

Recommended orchestrator choice: **Option A — Dedicated Orchestrator Container App**.

Justification:

- Best fit for long-running Python agent framework code and Dapr sidecars.
- Same hosting, scaling, identity, and observability model as the custom agents.
- Easier local parity with Docker Compose than Durable Functions.
- Supports both synchronous APIs and async Dapr pub/sub patterns.

Alternatives:

- **Durable Functions**: strong for event-sourced workflows and timers, but less natural for Dapr sidecars and custom AI runtime dependencies.
- **Manager Agent in ACA**: useful later as an LLM-based planner, but the production control plane should be deterministic, testable, and API-first.

Agent framework recommendation:

- Use **Semantic Kernel + Azure OpenAI** for managed tool/function calling where the orchestrator owns planning.
- Support **Azure AI Agent Service** through an adapter for managed agents.
- Keep a **custom implementation seam** for containerized agents so Hermes/OpenClaw-style runtimes are isolated behind `GET /health` and `POST /execute`.

## 3. Infrastructure as Code

Bicep modules in `infra/` provision:

- Azure Container Apps Environment with Log Analytics.
- Azure Container Registry for all images.
- Azure Cosmos DB for workflow state, checkpoints, and memory.
- Azure Key Vault for secrets.
- Azure OpenAI account and model deployment.
- Application Insights + Log Analytics.
- Managed identities for ACA apps.
- Dapr state and pub/sub components.

Key files:

```text
infra/main.bicep
infra/modules/container-app.bicep
infra/modules/cosmos-db.bicep
infra/modules/dapr-components.bicep
infra/modules/openai.bicep
infra/modules/service-bus.bicep
infra/modules/orchestrator-access.bicep
```

## 4. Agent Code Structure

Recommended folder structure:

```text
src/maf-orchestrator/
  app/
    main.py
    config.py
    agents/
      dapr_agent_client.py
      hermes_client.py
      openclaw_client.py
    workflows/
      task_router.py
    state/
      cosmos_state_store.py
    tools/
      common.py
  tests/

agents/
  hermes-agent/
    src/main.py
  openclaw-agent/
    src/main.py
  templates/python-agent/
    src/main.py
```

The base custom agent contract is intentionally small:

```http
GET /health
POST /execute
{
  "prompt": "...",
  "context": {}
}
```

Specialized agents differ by capability metadata and runtime command, not by orchestrator coupling.

## 5. Orchestrator Implementation

The orchestrator remains a FastAPI app hosted in ACA with Dapr enabled. It routes tasks by capability, invokes agents via Dapr service invocation when available, and falls back to direct HTTP endpoints for local development or external managed services.

Core behaviors:

- `/health`: liveness.
- `/tasks`: task submission alias.
- `/orchestrate`: plan, route, execute, checkpoint, and return a structured result.
- Capability routing through `ROUTE_CONFIG_JSON`.
- Dapr invocation through `DAPR_HTTP_PORT` and per-agent app IDs.

## 6. Dapr Configuration

Dapr usage:

- **Service invocation**: orchestrator → `researcher-agent`, `coder-agent`, `executor-agent`, `reviewer-agent`, `hermes-agent`, `openclaw-agent`.
- **State management**: `workflow-state` component backed by Cosmos DB.
- **Pub/Sub**: `agent-events` component backed by Azure Service Bus.

Component naming:

```text
workflow-state   # Dapr state store
agent-events     # Dapr pub/sub component
```

## 7. Deployment Guide

1. Build and push images to ACR.
2. Deploy infrastructure:

```bash
az deployment sub create \
  --location eastus \
  --template-file infra/main.bicep \
  --parameters environment=dev suffix=pantheon01
```

3. Update ACA revisions with image tags.
4. Verify health:

```bash
curl https://<orchestrator-fqdn>/health
```

5. Submit a smoke task:

```bash
curl -X POST https://<orchestrator-fqdn>/orchestrate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Research the deployment and also review the implementation"}'
```

## 8. Security & Best Practices

- Use managed identity for Cosmos DB, Key Vault, Azure OpenAI, and ACR pulls.
- Store no keys in source or app settings unless absolutely required for local development.
- Prefer internal ingress for agent Container Apps; expose only the orchestrator publicly.
- Do not log raw prompts or secrets.
- Use Dapr mTLS and ACA environment boundaries for service-to-service traffic.
- Use private networking/private endpoints for sensitive production deployments.
- Apply least-privilege role assignments per app identity.

## 9. Potential Improvements & Future Enhancements

- Replace deterministic keyword routing with an Azure OpenAI/Semantic Kernel planner.
- Add Azure AI Agent Service adapters for fully managed Researcher/Coder/Reviewer agents.
- Add event-driven long-running workflows over Dapr pub/sub.
- Add human-in-the-loop approval checkpoints.
- Add vector memory with Azure AI Search or Cosmos DB vector indexing.
- Add per-agent scale rules and queue-depth based KEDA triggers.
- Add OpenTelemetry trace correlation across Dapr sidecars and app spans.
