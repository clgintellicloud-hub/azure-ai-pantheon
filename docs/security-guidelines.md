# Guidelines for GitHub Repo & GitHub Actions Security

(No Credentials, Passwords, Tokens, or Personal Information in the Repository)

These guidelines should be followed by anyone (including AI assistants like Grok) when building, modifying, or maintaining the repository and its GitHub Actions workflows. The goal is zero secrets in git history.

## 1. Core Golden Rules (Never Do These)

Never commit any file containing real credentials, API keys, tokens, passwords, connection strings, private keys, certificates, or personal information.

Never hardcode secrets in source code, Dockerfiles, Bicep/Terraform files, compose.yaml, scripts, or workflow files.

Never echo, log, or print secrets in GitHub Actions runs (even temporarily).

Never commit .env files, local.settings.json, or any local configuration files that contain real values.

Never use long-lived service principal secrets or personal access tokens when OIDC / Workload Identity Federation is available.

Never put real values in committed parameter files (e.g., infra/parameters/*.json).

## 2. Repository Configuration (One-Time Setup – Do This Immediately)

In your repository Settings → Code security and analysis:

- Enable Secret scanning (GitHub Advanced Security)
- Enable Push protection (this is critical — it blocks pushes that contain secrets)
- Enable Dependabot alerts and Dependabot security updates
- Enable Code scanning (CodeQL) if possible

Also enable:

- Branch protection rules on main (and important branches)
- Require pull request reviews before merging
- Require status checks to pass before merging

## 3. Required .gitignore Entries

Your .gitignore must include at minimum:

```gitignore
# Secrets & Environment
.env
.env.*
*.env
.envrc

# Local development / IDE
.vscode/
.idea/
*.code-workspace
local.settings.json
appsettings.Development.json

# Azure / azd local state
.azure/
azd/
**/*-local.json
**/*-dev.json

# Keys and certificates
*.pem
*.key
*.crt
*.pfx
secrets/
credentials/

# Python
__pycache__/
*.py[cod]
.venv/
venv/
.env.local

# Node / others (if applicable)
node_modules/
```

## 4. GitHub Actions Security Rules (Critical)

When creating or modifying workflows in .github/workflows/:

| Rule | Requirement | Why |
|------|-------------|-----|
| OIDC First | Use OIDC / Workload Identity Federation for Azure (via azure/login action). Never store client secrets. | Eliminates long-lived credentials |
| permissions | Always declare minimal permissions at workflow or job level | Prevents over-privileged GITHUB_TOKEN |
| Action Pinning | Pin all third-party actions to full commit SHA (not @v4 or @main) | Prevents supply-chain attacks |
| Secrets Access | Only use ${{ secrets.XXX }} or ${{ vars.XXX }}. Never hardcode values | Secrets are redacted in logs |
| Environment Secrets | Use Environment secrets + protection rules for production deployments | Adds approval gates |
| No Interpolation | Never put ${{ github.event.* }} or untrusted input directly into run: steps | Prevents injection attacks |
| Masking | Use ::add-mask:: only when absolutely necessary | Better to avoid logging secrets entirely |
| Least Privilege | Each workflow/job should only have access to the secrets it actually needs | Limit blast radius |

### Example of correct Azure OIDC login pattern (preferred):

```yaml
permissions:
  id-token: write
  contents: read

- uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

## 5. IaC & Application Code Rules

- **Bicep / Terraform**: Never hardcode secrets. Use parameters + Key Vault references or Managed Identities.
- **Dockerfiles**: Never copy .env files or bake secrets into images. Use runtime environment variables or mounted secrets.
- **Python / Application code**: Load secrets only from environment variables or secure secret managers (Azure Key Vault, etc.). Use libraries like azure-identity.
- **compose.yaml**: Never include real credentials. Use variable substitution or external secret files (gitignored).
- **Parameter files (infra/parameters/)**: Only commit non-sensitive values. Sensitive values should come from GitHub Secrets / Environment variables or Key Vault at deploy time.

## 6. Local Development Practices

- Always use .env files for local development — these must be in .gitignore.
- Document in README.md or docs/local-development.md exactly how to set up local secrets (e.g., "Copy .env.example to .env and fill in values").
- For azd: Use azd env set for local environment variables (they are stored locally and not committed).
- Never share screenshots or logs that contain real secrets.

## 7. Guidelines Specifically for AI Assistants (Grok, Copilot, etc.)

When asking an AI to generate or modify code for this repository, include these instructions:

> "You are working on a secure GitHub repository. Follow these strict rules:
> 
> Never output real credentials, tokens, or example secret values.
> 
> Always reference secrets using ${{ secrets.NAME }} (GitHub Actions) or environment variables.
> 
> For Azure deployments, prefer and generate OIDC-based authentication using the azure/login action with client-id / tenant-id from vars (not secrets).
> 
> When creating new files, recommend appropriate additions to .gitignore.
> 
> Add security comments in generated code/workflows (e.g., # Store value in GitHub Secrets as AZURE_CLIENT_ID).
> 
> For Bicep or infrastructure code, use parameters and never hardcode connection strings or keys.
> 
> If generating local development instructions, always tell the user to use gitignored .env files."

## 8. GitHub Platform Best Practices (Enable These)

| Feature | Recommendation | Benefit |
|---------|----------------|---------|
| Secret scanning + Push protection | Enable at repo + org level | Blocks secrets before they enter git history |
| Dependabot | Enable for all ecosystems | Keeps actions and dependencies updated |
| Code scanning (CodeQL) | Enable | Catches insecure patterns automatically |
| Branch protection | Require reviews + status checks | Prevents direct pushes to main |
| Environments | Create dev, staging, production with required reviewers | Adds approval gates for secrets |
| CODEOWNERS | Use for sensitive paths (.github/, infra/) | Ensures security-conscious reviewers |
| Signed commits | Encourage / require where possible | Improves auditability |

## 9. Azure-Specific Recommendations (for This Project)

- Use Managed Identities everywhere possible (ACA, Azure Functions, etc.).
- For GitHub Actions → Azure: Use OIDC federation (Workload Identity Federation) — this is the modern standard and eliminates the need to store client secrets.
- Store non-secret configuration in GitHub Variables (vars) and only true secrets in Secrets.
- Use Azure Key Vault references in Bicep where appropriate.
- For ACA deployments: Pass secrets via secure environment variables or Key Vault references, never in image layers.

## Recommended Files to Add to Repo

- `SECURITY.md` — High-level security policy
- `docs/security-guidelines.md` — This document (or a shortened version)
- `.github/secret_scanning.yml` (optional) — To define custom patterns or exclusions
