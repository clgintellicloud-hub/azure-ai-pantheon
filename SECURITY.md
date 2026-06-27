# Security Policy

## Supported Versions

We take security seriously. Currently, only the latest version of the main branch is supported for security updates.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately by contacting the repository owner.

**Please do not open public issues for security vulnerabilities.**

## Guidelines

This repository follows strict security practices:

- No credentials, tokens, passwords, or secrets in the repository or git history.
- All GitHub Actions use OIDC / Workload Identity Federation for Azure where possible.
- Secret scanning and push protection are enabled.
- Follow the guidelines in `docs/security-guidelines.md`.

## Responsible Disclosure

We appreciate responsible disclosure and will acknowledge contributions where appropriate.
