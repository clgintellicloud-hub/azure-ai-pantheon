# Local Development

## Secrets Management

**Never commit real secrets to the repository.**

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your local values.

3. The `.env` file is gitignored (see `.gitignore`).

## For Azure / MAF Development

- Prefer Managed Identity when possible.
- For local testing of GitHub Actions patterns, you can use service principal credentials temporarily in your `.env` only.
- In CI/CD, always use OIDC (see `.github/workflows/` and `docs/security-guidelines.md`).

## Using azd (Azure Developer CLI)

```bash
azd env set AZURE_SUBSCRIPTION_ID your-id
azd env set FOUNDRY_ENDPOINT https://...
```

These are stored locally by azd and not committed.

## Running Locally - End-to-End Demo

```powershell
# 1. Prepare environment (mocks work with defaults)
copy .env.example .env

# 2. Start everything (orchestrator + mock Hermes + mock OpenClaw)
docker compose up --build

# 3. In another terminal, test the full flow:

# Health check
Invoke-RestMethod http://localhost:8000/health

# Example 1: Triggers Hermes (analysis keywords)
Invoke-RestMethod -Method Post -Uri http://localhost:8000/tasks -Body (@{prompt="Analyze this complex strategy problem"} | ConvertTo-Json) -ContentType "application/json"

# Example 2: Triggers OpenClaw (general execution)
Invoke-RestMethod -Method Post -Uri http://localhost:8000/tasks -Body (@{prompt="Help me book a flight and send an email"} | ConvertTo-Json) -ContentType "application/json"

# Example 3: Triggers both
Invoke-RestMethod -Method Post -Uri http://localhost:8000/orchestrate -Body (@{prompt="Research the market and also execute the outreach plan"} | ConvertTo-Json) -ContentType "application/json"

# Example 4: Receive a webhook payload and route it as an orchestration task
Invoke-RestMethod -Method Post -Uri http://localhost:8000/webhooks/github -Body (@{event="issue.created"; issue=@{title="Research Dapr webhook ingress"}} | ConvertTo-Json -Depth 4) -ContentType "application/json"
```

You should see in the logs:
- Planning step
- Handoff to HermesAgent / OpenClawAgent
- Results from the agents

The response will include the plan and execution details.

## Webhook Payload Ingress

The orchestrator accepts JSON payloads at:

```text
POST /webhooks/{source}
```

Examples:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:8000/webhooks/github `
  -Headers @{"X-Pantheon-Event"="issue.created"} `
  -Body (@{event="issue.created"; issue=@{title="Research Dapr webhook ingress"}} | ConvertTo-Json -Depth 4) `
  -ContentType "application/json"
```

For signed local testing, set `WEBHOOK_SHARED_SECRET` in `.env` and send `X-Pantheon-Signature-256` or `X-Hub-Signature-256` with `sha256=<HMAC hex digest>` over the raw request body.

For faster Python-only dev (without Docker):
```powershell
cd src/maf-orchestrator
pip install -r requirements.txt
uvicorn app.main:app --reload
```
(Note: the mock agents need to be running separately for full end-to-end.)

## Security Reminders

- Never share logs or screenshots containing real values.
- Follow all rules in `docs/security-guidelines.md`.
