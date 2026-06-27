# Project Status — azure-ai-pantheon

**Date**: 2026-06-27

## High-Level State
- Repository freshly initialized by cloning from GitHub.
- Only minimal README + this documentation structure.
- No production code yet in this repo.

## Background Context (to survive reboots)
The user wants to use **Microsoft Agent Framework (MAF)** to orchestrate and manage instances of two popular third-party autonomous agents:
- Hermes Agent (Nous Research)
- OpenClaw

These agents are currently being run inside **Azure Container Apps** using existing IaC from sibling projects (`azure-hermes-factory` and `oc-agent-main`).

This repo (`azure-ai-pantheon`) is intended to become the higher-level orchestration / management / "pantheon" system.

## Immediate Next Actions (Typical)
1. Study the existing factories (Bicep, Docker wrappers, agent configs).
2. Explore current MAF capabilities for ACA deployments and multi-agent workflows.
3. Design the architecture for Pantheon (MAF as conductor talking to Hermes/OpenClaw runtimes).
4. Decide on language for MAF layer (Python vs .NET).
5. Evolve or replace parts of the current containerization approach.

## How This File Helps
Update this file (or create dated snapshots) whenever major progress is made. Combined with `AGENTS.md`, a fresh Grok session can understand where we left off.

## Key Files to Review in a New Session
- Root: `AGENTS.md`, `README.md`
- This file: `docs/STATUS.md`
- Related external: the two factory repositories mentioned in AGENTS.md

---

Update this section with current tasks, blockers, and decisions as work progresses.
