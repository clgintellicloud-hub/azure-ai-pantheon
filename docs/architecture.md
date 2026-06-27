# Recommended Azure Architecture for MAF-based Orchestration of Hermes + OpenClaw Agents

You want a production-grade orchestration layer built with Microsoft Agent Framework (MAF) that coordinates your existing Hermes and OpenClaw agents, all running scalably in Azure. MAF (from microsoft/agent-framework) is an excellent fit — it is a first-class, multi-language (.NET + Python) framework specifically designed for production multi-agent workflows, with strong orchestration (graph-based workflows, handoff, concurrent/sequential patterns, checkpointing), OpenTelemetry observability, and native integration with Microsoft Foundry.

## Core Recommended Azure Services

| Service | Role | Why It Fits Best | Key Benefits for Your Use Case |
|---------|------|------------------|--------------------------------|
| **Azure Container Apps (ACA)** | Primary runtime for everything | Purpose-built for containerized agents & microservices. Supports Compose for Agents (preview), autoscaling, revisions, Dapr, and easy ingress. | Run MAF orchestrator + Hermes + OpenClaw as independent, scalable containers. Pay-per-second. Recent agent-focused features (model runners, MCP gateways). |
| **Microsoft Foundry (Azure AI Foundry / Foundry Agent Service)** | Models, tools, observability & optional hosted runtime | Deep MAF integration (FoundryChatClient / AIProjectClient). Rich traces, evals, planning visualization. | MAF agents emit standardized gen_ai.* spans → beautiful agent traces in Foundry. Centralized model management + tool registry. |
| **Azure Cosmos DB** | Workflow state, checkpoints, history & memory | Serverless, global scale, change feed. Excellent for durable workflows. | Store MAF workflow state, task plans, agent decisions, long-term memory. Complements or replaces parts of your existing Postgres/pgvector if desired. |
| **Azure Container Registry (ACR)** | Image repository | Native, secure image storage with Managed Identity integration. | Versioned images for orchestrator + Hermes + OpenClaw with easy rollback. |
| **Azure Key Vault + Managed Identities** | Secrets & auth | Passwordless everywhere. | Store LLM keys, connection strings, etc. All services (ACA, Foundry, Cosmos) use Managed Identity. |
| **Azure Monitor + Application Insights** | Telemetry | OpenTelemetry sink that feeds Foundry. | Distributed tracing across MAF orchestrator ↔ Hermes ↔ OpenClaw. |

### Optional but valuable additions

- **Azure App Service** (or a lightweight ACA frontend) — Simple web dashboard for task submission, monitoring, and human-in-the-loop.
- **Azure Service Bus** or ACA Dapr pub/sub — Reliable async messaging between orchestrator and agents.
- **Bicep** (via Azure Developer CLI / azd) — For all infrastructure.

## Why this stack over alternatives?

- **AKS** → Too much operational overhead for this workload.
- **Azure Functions alone** → Great for lightweight pieces but containers give you full control over the MAF runtime and your custom agents.
- **Logic Apps / Durable Functions** → Good for simpler flows; MAF + ACA gives you code-first power + durability via checkpointing + Cosmos.
- **Pure Foundry Agent Service (no-code)** → Excellent for standard agents, but you want custom orchestration logic and full control over Hermes/OpenClaw integration → MAF in ACA is the code-first path shown in Microsoft’s own multi-agent reference architecture.

## High-Level Architecture

- **User / Trigger** → Submits task (via dashboard, API, webhook, or scheduled job).
- **MAF Orchestrator (ACA)** → Receives request, uses MAF workflows to decompose task, plans, and coordinates.
- **MAF calls Hermes and/or OpenClaw** (via HTTP APIs, MCP tools, function calling, or handoff patterns). You expose your existing agents as tools/skills or standardized endpoints.
- **Agents execute** (in their own ACA instances — isolated scaling, different resource profiles if needed).
- **State & Memory** → Cosmos DB (or your Postgres) + MAF checkpointing.
- **Observability** → All components emit OpenTelemetry → Application Insights → rich visualization in Foundry.
- **Models** → Served via Foundry (or Azure OpenAI directly).

You can start with individual ACA apps for maximum isolation/scaling control, or explore **Compose for Agents** (preview) with a single compose.yaml that declares multiple agents + model runners.

## GitHub Repository File Structure (IaC vs Software Separation + Controllable Deployments)

This structure gives you clean separation, path-triggered GitHub Actions, reusable Bicep modules, and easy azd support.

```
maf-orchestration/                          # Repo name suggestion: maf-hermes-orchestration or annapurna-maf-agents
├── .github/
│   └── workflows/
│       ├── ci.yml                          # Lint, test, build on PRs (path filtered)
│       ├── deploy-iac.yml                  # Bicep deploy (manual or infra/** changes)
│       ├── deploy-orchestrator.yml         # Build + push MAF image → update ACA (src/** or dispatch)
│       ├── deploy-hermes.yml               # Hermes agent updates
│       ├── deploy-openclaw.yml             # OpenClaw agent updates
│       ├── deploy-all.yml                  # Full environment deploy (workflow_dispatch with inputs)
│       └── reusable/                       # Composite actions or reusable workflows
├── infra/                                  # ← Pure IaC (completely separate from code)
│   ├── main.bicep                          # Top-level composition
│   ├── modules/
│   │   ├── aca-environment.bicep
│   │   ├── container-app.bicep             # Reusable module for orchestrator/hermes/openclaw
│   │   ├── cosmos-db.bicep
│   │   ├── key-vault.bicep
│   │   ├── acr.bicep
│   │   ├── monitoring.bicep
│   │   └── foundry.bicep                   # (optional) Foundry project + model deployment
│   └── parameters/
│       ├── dev.bicepparam
│       └── prod.bicepparam
├── src/                                    # ← MAF Orchestrator application code
│   ├── maf-orchestrator/                   # Main Python (or .NET) project
│   │   ├── app/
│   │   │   ├── main.py                     # FastAPI/Starlette entrypoint + MAF workflows
│   │   │   ├── workflows/                  # MAF graph-based orchestrations
│   │   │   ├── agents/                     # Wrappers/clients for Hermes & OpenClaw
│   │   │   ├── tools/                      # MAF tools/skills (including calls to your agents)
│   │   │   └── middleware/                 # Logging, auth, error handling, human-in-loop
│   │   ├── Dockerfile
│   │   ├── pyproject.toml (or requirements.txt)
│   │   └── tests/
│   └── shared/                             # Common utilities / Pydantic models
├── agents/                                 # Container sources for your existing agents
│   ├── hermes-agent/
│   │   ├── Dockerfile
│   │   └── src/...
│   └── openclaw-agent/
│       ├── Dockerfile
│       └── src/...
├── compose.yaml                            # Local Docker Compose (mirrors production)
├── azd.yaml                                # Azure Developer CLI config (strongly recommended)
├── README.md
├── .gitignore
└── docs/
    ├── architecture.md
    └── runbooks/
```

## Why this structure excels for your requirements

- **IaC completely separated** (infra/) — Changes to Bicep never accidentally trigger app builds.
- **Controllable deployments** — GitHub Actions use paths filters + workflow_dispatch (with inputs like "deploy which component?"). You can run individual agent deploys or full IaC + app pipelines.
- **Reusable modules** — One container-app.bicep module parameterized for orchestrator vs. Hermes vs. OpenClaw (different CPU/memory, scaling rules, env vars).
- **azd-friendly** — azd up provisions everything and deploys the orchestrator (and optionally agents). Many existing azd templates already combine ACA + MAF + Foundry.
- **Local ↔ Cloud parity** — compose.yaml works locally; ACA Compose preview can consume similar declarations.
- **Future-proof** — Easy to add more agents later.

## Language Recommendation for MAF

Python is the stronger starting point for you (matches your existing Hermes/OpenClaw/Python-heavy stack, faster iteration, rich MAF samples). .NET is equally capable if you prefer strong typing or have C# experience. Both support Foundry hosting with ~2 lines of code change.

## Next Steps & Considerations

- **Start small** — Create the MAF orchestrator as a simple FastAPI + MAF workflow that can call Hermes/OpenClaw via HTTP or as MAF tools.
- **Instrument everything with OpenTelemetry early** (MAF has built-in support).
- **Use Managed Identity everywhere** — no secrets in env vars or code.
- **State strategy** — Decide how much lives in MAF checkpoints + Cosmos vs. your existing Postgres.
- **Cost control** — ACA + serverless Cosmos + pay-per-token Foundry models keep this efficient. Set scaling rules and budgets.
- **Security** — Private endpoints / VNet for ACA environment if handling sensitive data. App Insights + Foundry for auditability.

This architecture aligns directly with Microsoft’s published multi-agent reference architecture (MAF in Container Apps + Foundry + Cosmos) while giving you full control over your custom Hermes and OpenClaw agents.
