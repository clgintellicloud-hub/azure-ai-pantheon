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

## Running Locally

```bash
# With Docker Compose
docker compose up --build

# Or directly
cd src/maf-orchestrator
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Security Reminders

- Never share logs or screenshots containing real values.
- Follow all rules in `docs/security-guidelines.md`.
