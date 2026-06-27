# AGENTS.md

> **This file exists so that any future Grok (or other AI coding agent) session can quickly recover full project context after a computer reboot, new terminal, or new conversation.**

## Project Identity
- **Name**: azure-ai-pantheon
- **Tagline**: AI Agent orchestration
- **Repo**: https://github.com/clgintellicloud-hub/azure-ai-pantheon.git
- **Workspace Path**: `C:\Users\openclaw\Documents\grok`
- **Purpose**: Build a management and orchestration layer ("Pantheon") for multiple AI agents — specifically **Hermes Agent** and **OpenClaw** — running as containerized workloads inside **Azure Container Apps (ACA)**, with **Microsoft Agent Framework (MAF)** as a primary orchestration technology.

## Core Objective
Create a system that can:
- Deploy, manage, version, scale, and observe Hermes and OpenClaw agents on ACA.
- Use Microsoft Agent Framework (MAF) for higher-level coordination, workflows, routing between agent types, unified interfaces, and observability.
- Act as the "conductor" or meta-orchestrator on top of the lower-level agent runtimes.

## Current State (as of 2026-06-27)
- Repository was just cloned into this directory.
- Contains only an initial commit with a minimal README.
- No application code, infrastructure, or detailed docs yet in this repo.
- Active development workspace is this folder.

## Critical Related Codebases (Prior Work)
These contain existing patterns the Pantheon should build upon or evolve:

1. **Azure Hermes Factory**  
   Path: `C:\Users\openclaw\Documents\claude-code\azure-hermes-factory\`  
   - Bicep-based IaC for ACA (dev + prod resource groups)  
   - ACR, Container Apps Environment, multiple agents  
   - Dockerized wrappers for Hermes + "analyst" + generic OpenClaw-style agents  
   - Uses Node.js HTTP shim that spawns the real `hermes-agent` CLI  
   - Scripts for build, revisions, rollback, smoke tests

2. **OC Agent Main**  
   Path: `C:\Users\openclaw\Downloads\oc-agent-main\oc-agent-main\`  
   - Very similar structure to the above, more OpenClaw-focused configs

These two should be studied when designing the Pantheon layer.

## Key Technologies
- **Microsoft Agent Framework (MAF)** — Primary framework for the orchestration layer (Python and/or .NET). Unifies concepts from Semantic Kernel + AutoGen. Supports workflows, agents, middleware, sessions, MCP, strong telemetry.
- **Azure Container Apps (ACA)** — Runtime platform for the individual Hermes/OpenClaw containers and potentially MAF orchestrators.
- **Hermes Agent** (Nous Research) — Self-improving autonomous agent with skills, learning loop, memory. Currently wrapped and deployed via the factories.
- **OpenClaw** — Another popular autonomous agent platform being run side-by-side.
- **Bicep** — Current IaC language.
- **Docker** — For packaging agents.
- **Microsoft Foundry** — Likely target for observability and higher-level agent features.
- GitHub CLI (`gh`) — Already authenticated as `clgintellicloud-hub`.

## Architecture Direction (Early Thinking)
- Lower layer: Existing containerized Hermes and OpenClaw instances on ACA (from the factories).
- Orchestration layer: MAF agents/workflows that can discover, invoke, route to, monitor, and compose the above agents.
- Possible patterns:
  - MAF as supervisor / router
  - Hermes/OpenClaw exposed via HTTP or MCP and treated as tools or sub-agents
  - Unified control plane for versioning, scaling, A/B testing (leveraging ACA revisions)
  - Strong observability (OTel → Application Insights → Foundry)

## How to Resume Work After Reboot or New Session
When you (Grok or another agent) start fresh:

1. Change to the project directory:
   ```powershell
   cd "C:\Users\openclaw\Documents\grok"
   ```

2. **Read the following files first** (in this order):
   - `AGENTS.md` (this file)
   - `README.md`
   - Any files under `docs/`

3. Explore the filesystem:
   ```powershell
   Get-ChildItem -Force
   Get-ChildItem -Recurse -Depth 2
   ```

4. Review prior work (very important):
   - List and read key files from `..\claude-code\azure-hermes-factory\`
   - Review the `oc-agent-main` folder

5. Ask the user or review recent commits for the latest task.

6. (Recommended) Run any local resume helper if present:
   ```powershell
   .\scripts\resume-context.ps1
   ```

## Documentation Conventions in This Repo
- `AGENTS.md` — Primary context file for AI agents (update this often).
- `README.md` — High-level for humans + points to AGENTS.md.
- `docs/` — Detailed architecture, decisions, status, runbooks.
- Keep status, decisions, and current goals in committed Markdown files.
- Update this file whenever major context changes (architecture decisions, new related code locations, major progress).

## Recommended Practices
- Commit context files early and often (`AGENTS.md`, `docs/*.md`).
- Use clear, self-contained Markdown so a fresh session can understand the project without the full chat history.
- When making progress, summarize changes back into `docs/STATUS.md` or this file.
- For task tracking, prefer files in `docs/` or `TODO.md` alongside any in-session todo tools.

## Contact / Ownership
- GitHub account context: `clgintellicloud-hub`
- User frequently works with Hermes, OpenClaw, and Azure agent deployments.

---

**Last updated**: 2026-06-27 (initial creation to preserve context across sessions)

**Next step for any new session**: Read this file completely, then explore the related factory directories.
