# AGENTS.md

> **This file exists so that any future Grok (or other AI coding agent) session can quickly recover full project context after a computer reboot, new terminal, or new conversation.**

## Project Identity
- **Name**: azure-ai-pantheon
- **Tagline**: AI Agent orchestration
- **Repo**: https://github.com/clg-built4tech-azure/azure-ai-pantheon.git
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
These contain existing patterns the Pantheon should build upon or evolve. Full source for prior work lives in the related sibling projects `azure-hermes-factory` and `oc-agent-main`.

See:
- `docs/EXISTING_FACTORIES_ANALYSIS.md` — Detailed comparison and implications
- `docs/KNOWN_PRIOR_WORK.md` — Summary of patterns from those projects

Key patterns observed:
- Bicep-based IaC for ACA (dev + prod)
- ACR + Log Analytics + Container Apps
- Dockerized wrappers that spawn the real Hermes/OpenClaw agent CLI
- Scripts for revisions, rollback, and smoke tests

These should be studied when designing the Pantheon layer.

## Key Technologies
- **Microsoft Agent Framework (MAF)** — Primary framework for the orchestration layer (Python and/or .NET). Unifies concepts from Semantic Kernel + AutoGen. Supports workflows, agents, middleware, sessions, MCP, strong telemetry.
- **Azure Container Apps (ACA)** — Runtime platform for the individual Hermes/OpenClaw containers and potentially MAF orchestrators.
- **Hermes Agent** (Nous Research) — Self-improving autonomous agent with skills, learning loop, memory. Currently wrapped and deployed via the factories.
- **OpenClaw** — Another popular autonomous agent platform being run side-by-side.
- **Bicep** — Current IaC language.
- **Docker** — For packaging agents.
- **Microsoft Foundry** — Likely target for observability and higher-level agent features.
- GitHub CLI (`gh`) — Ensure `gh` is authenticated to your current account (`clg-built4tech-azure`).

## Architecture Direction (Guiding Document)
Follow the full recommended architecture:
- **[docs/architecture.md](docs/architecture.md)** — Production Azure stack (ACA primary runtime, Microsoft Foundry, Cosmos DB for state, ACR, Key Vault + Managed Identity, App Insights).
- High-level flow: User/Trigger → MAF Orchestrator (ACA) → calls Hermes/OpenClaw agents (in their own ACA containers) → state in Cosmos + MAF checkpoints → full OTel traces in Foundry.
- Repository structure: Strict separation of `infra/` (Bicep) and `src/` (MAF code) with path-filtered GitHub Actions for controllable deployments.
- See also: `docs/EXISTING_FACTORIES_ANALYSIS.md` for analysis of prior work this architecture builds upon.

Key implementation goals:
- MAF workflows for orchestration, handoff, and tool calling to existing agents.
- Expose Hermes/OpenClaw as MAF tools or via standardized endpoints (HTTP/MCP).
- Use ACA revisions + Compose for Agents (preview) where appropriate.

## How to Resume Work After Reboot or New Session
When you (Grok or another agent) start fresh:

1. Change to the project directory:
   ```powershell
   cd <project-root>
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
   - Read `docs/EXISTING_FACTORIES_ANALYSIS.md` and `docs/KNOWN_PRIOR_WORK.md`
   - These describe patterns from the related `azure-hermes-factory` and `oc-agent-main` projects

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

## Security Guidelines for AI Assistants

This repository follows strict security rules (see `docs/security-guidelines.md`).

When generating or modifying code, workflows, or IaC:

- **Never** output real credentials, tokens, example secret values, or personal information.
- Always reference secrets using `${{ secrets.NAME }}` (GitHub Actions) or environment variables.
- For Azure: Prefer and generate **OIDC-based authentication** using the `azure/login` action with `client-id` / `tenant-id` from `vars` (not secrets).
- When creating new files, recommend appropriate additions to `.gitignore`.
- Add security comments in generated code (e.g. `# Store value in GitHub Secrets as AZURE_CLIENT_ID`).
- For Bicep/infra: Use parameters. Never hardcode connection strings or keys.
- For local development instructions: Always tell the user to use gitignored `.env` files.
- Follow all rules in `docs/security-guidelines.md` and `SECURITY.md`.

## Routine Context Saving Protocol (Critical for No Data Loss)

This is the **official process** to ensure almost nothing important is lost after a reboot or new session.

### 1. Primary Files That Must Stay Current
- `docs/LIVE_STATE.md` — The single source of "what is happening RIGHT NOW". Short, scannable, frequently overwritten with latest status.
- `docs/SESSION_LOG.md` — Append-only historical record of work sessions.
- `AGENTS.md` — Only updated for major structural changes (new related repos, big architecture shifts, etc.).
- `docs/DECISIONS.md` — Record important "why" decisions as they are made.
- `docs/STATUS.md` — Higher-level overview (less frequently updated than LIVE_STATE).

### 2. When to Save Context (The Triggers)
Save context **routinely** at these points:
- End of a focused work block (e.g., "I just finished analyzing the Bicep modules").
- After any significant decision or discovery.
- Before ending a long session or when the user says "save context", "update state", or "commit the memory".
- At the end of implementing a feature or fixing something important.

### 3. How to Save (The Method)
**Preferred method (agent or human):**
```powershell
cd <project-root>
powershell -ExecutionPolicy Bypass -File .\scripts\save-context.ps1 `
  -Summary "Summarized what was just accomplished" `
  -FocusArea "MAF research / Hermes factory analysis" `
  -NextSteps "Next step 1\nNext step 2"
```

The script will:
- Update `docs/LIVE_STATE.md` with the new current state and timestamp.
- Append a structured entry to `docs/SESSION_LOG.md`.
- Stage the important context files.
- Print a suggested git commit message.

**Alternative (direct agent action):**
I can directly edit `docs/LIVE_STATE.md` and append to `docs/SESSION_LOG.md` using tools, then stage + commit. This is often cleaner during active work.

### 4. Git Discipline
- Context changes should almost always be committed.
- Use clear messages starting with `chore(context): ...`
- This makes `git log` itself a useful recovery tool.

### 5. Agent Behavior Rules (For Me)
When I am working on this project:
- I will proactively keep `docs/LIVE_STATE.md` accurate.
- After any non-trivial progress, I will either run the save script or directly update the live state files.
- At the end of my response, if meaningful work happened, I will offer: "Would you like me to save the current context now?"
- I will not rely solely on chat history.

### 6. User Actions That Help
- Say "save context" or "update live state" at natural stopping points.
- Review `docs/LIVE_STATE.md` occasionally and correct anything that feels outdated.
- Do not delete or heavily refactor these files without updating the protocol in this AGENTS.md.

Following this protocol means that even if the entire conversation history disappears, a new session that reads `AGENTS.md` + `docs/LIVE_STATE.md` + recent SESSION_LOG entries will have excellent continuity.
- For task tracking, prefer files in `docs/` or `TODO.md` alongside any in-session todo tools.

## Branching Strategy

**All feature branches MUST use the `grok/` prefix.**

### Rules
- `main` remains `main` (never prefixed).
- Feature, enhancement, fix, refactor, docs, etc. branches must be named:
  - `grok/<kebab-case-description>`
- Examples:
  - `grok/add-maf-orchestrator`
  - `grok/hermes-openclaw-integration`
  - `grok/improve-aca-deployment`
  - `grok/context-persistence-updates`
- Never use bare names like `feature-x`, `my-work`, etc.

### How to Create a Feature Branch
Use the provided helper script (recommended):

```powershell
cd <project-root>
.\scripts\create-grok-branch.ps1 add-maf-orchestrator
# or with bypass if needed:
powershell -ExecutionPolicy Bypass -File .\scripts\create-grok-branch.ps1 "your-feature-name"
```

The script normalizes the name and enforces the `grok/` prefix.

Alternatively (manual):
```powershell
git checkout -b grok/your-feature-name
```

### Git Alias (Optional Convenience)
The alias is already configured in this working tree:
```powershell
git grok-branch add-maf-orchestrator
```

**Note**: The alias is basic and accepts only the feature name (it creates + checks out `grok/<name>`).  
For flags like `-NoCheckout`, call the script directly:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create-grok-branch.ps1 "add-maf-orchestrator" -NoCheckout
```

### Why the Prefix?
- Clearly identifies branches created as part of Grok-assisted development in this project.
- Makes it easy to filter and manage work in GitHub, PRs, and local checkout.
- Enforces team / agent consistency.

This rule applies to **all current and future feature branches**. If you see a non-`grok/` feature branch, rename it:
```powershell
git branch -m old-name grok/old-name
```

## Contact / Ownership
- GitHub account: `clg-built4tech-azure`
- User frequently works with Hermes, OpenClaw, and Azure agent deployments.

---

**Last updated**: 2026-06-27 (initial creation to preserve context across sessions)

**Next step for any new session**: Read this file completely, then explore the related factory directories.
