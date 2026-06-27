# Analysis of Existing Hermes / OpenClaw Factories

**Branch**: `grok/analyze-existing-factories`  
**Date**: 2026-06-27  
**Purpose**: Initial exploration of prior work that the azure-ai-pantheon (MAF orchestration layer) must understand and build upon.

## Overview

We have two closely related but distinct codebases that deploy Hermes Agent and OpenClaw-style agents to Azure Container Apps:

1. **azure-hermes-factory** (`~/Documents/claude-code/azure-hermes-factory/`)
2. **oc-agent-main** (`~/Downloads/oc-agent-main/oc-agent-main/`)

Both solve the same core problem: packaging autonomous agents (Hermes / OpenClaw) as containerized workloads on ACA with proper IaC, multi-environment support, and operational tooling.

## Common Patterns

### Deployment Model
- **Runtime**: The real agent (`hermes-agent` npm package) is installed globally in the container.
- **Wrapper**: A thin Node.js HTTP server (`src/agent.js`) acts as the entrypoint.
  - Spawns `hermes-agent gateway run ...` as a child process.
  - Exposes a `/health` endpoint.
  - Listens on port 8080 (for ACA ingress).
- **Configuration**: Minimal JSON (`hermes.json` or `openclaw.json`) defining model defaults.
- **Infrastructure**: Bicep templates targeting subscription scope.
  - Separate dev/prod resource groups.
  - Shared ACR (`ocrocagentdev`).
  - Log Analytics workspace.
  - ACA environments.
  - Dynamic "generic" agent instances via parameter (e.g. `hermes-ai-1`, `hermes-ai-2`).

### Agent Variants
Both factories support:
- `hermes` – Core agent
- `analyst` – Specialized analyst agent
- OpenClaw-style generic containers

### Key Technologies
- Node 22 base image
- Bicep for IaC
- Azure Container Apps (with revisions for versioning)
- Managed identity + ACR
- Smoke tests + rollback scripts

## Key Differences

| Aspect                    | azure-hermes-factory                          | oc-agent-main                                      |
|---------------------------|-----------------------------------------------|----------------------------------------------------|
| **Branding**              | Strongly "Hermes" focused                     | More OpenClaw / general                          |
| **CI/CD**                 | Scripts (build.sh, etc.)                      | GitHub Actions workflows (openclaw-deploy.yml, openclaw-infra.yml) |
| **IAM**                   | Separate `infra/iam/` modules                 | Similar but slightly different structure         |
| **Config Files**          | Uses `hermes.json`                            | Uses `openclaw.json` in the OpenClaw variant     |
| **Resource Groups**       | `rg-hermes-dev`, `rg-hermes-prod`             | `rg-openclaw-dev`, `rg-openclaw-prod`            |
| **ACA Env Names**         | `oclaw-env-dev`                               | Same naming pattern                              |
| **Scaling Param**         | `hermesAIContainerAppCount`                   | Not present in the sampled main.bicep            |
| **Workflow Features**     | Basic scripts                                 | Cost gate, manual approval gates, matrix deploys |

## Implications for azure-ai-pantheon (MAF Orchestration)

### What Pantheon Should Leverage
- The **wrapper pattern** (Node shim + real agent) is battle-tested and should probably be preserved or evolved.
- Existing Bicep modules are reusable for deploying new MAF-based orchestrators.
- Multi-revision ACA support is perfect for A/B testing different agent versions or MAF supervisors.
- Health endpoints already exist – good foundation for MAF to discover and monitor sub-agents.

### What Pantheon Must Improve / Add
1. **Orchestration Layer**
   - MAF agents/workflows that can route work to Hermes vs OpenClaw instances.
   - Unified interface / capability discovery across heterogeneous agents.

2. **Observability**
   - Current factories only do basic Log Analytics.
   - Need rich MAF + Foundry integration (gen_ai spans, tool calls, agent traces).

3. **Management Plane**
   - Higher-level control: scaling policies, version promotion, canary deployments across agent types.
   - Possibly a MAF "Pantheon Supervisor" that itself runs in ACA.

4. **Configuration**
   - Current configs are very thin. Pantheon should introduce richer agent profiles, routing rules, and MAF-specific config.

5. **Deployment Evolution**
   - The two factories have diverged slightly. Pantheon should aim for a unified or composable deployment story.

## Next Steps on This Branch

- [ ] Deep dive into Bicep modules (aca-environment, container-apps, etc.)
- [ ] Inspect GitHub Actions workflows from oc-agent-main
- [ ] Analyze the analyst and openclaw agent variants
- [ ] Identify extension points for MAF (HTTP APIs, MCP, A2A, etc.)
- [ ] Produce initial architecture recommendations for the Pantheon conductor

## References
- azure-hermes-factory main.bicep
- oc-agent-main main.bicep and workflows
- agents/*/src/agent.js (the critical wrapper)
- agents/*/Dockerfile

---

*This document is the first deliverable on the `grok/analyze-existing-factories` branch.*
