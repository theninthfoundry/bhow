# Deployment guide

## Scope of this repository-level deployment

This repository can publish a **static landing page** via GitHub Pages. It does **not** deploy the FastAPI backend in `bhow-v0.2/`.

- GitHub Pages here is for `index.html` and other static repository files only.
- Backend runtime services (API, database, auth provider) are separate and must be deployed to suitable infrastructure.

## GitHub Pages configuration and workflow source

The workflow at `.github/workflows/pages.yml` deploys a Pages artifact from the repository root on:

- push to `main`
- manual `workflow_dispatch`

Expected repository settings:

1. In GitHub repository settings, open **Pages**.
2. Set **Source** to **GitHub Actions**.
3. Do not configure branch-based Pages publishing for this setup.

## Verify Pages deployment after merge

After the PR merges to `main`:

1. Open **Actions** and confirm the "Publish static landing page" workflow completed successfully.
2. Open the deployed Pages URL shown in the `deploy` job output.
3. Verify the page states:
   - Bhow is a preview.
   - Content is educational and not veterinary diagnosis.
   - The backend is not yet a public production service.

If the workflow fails, inspect workflow logs before retrying.

## Backend deployment prerequisites (not included in Pages)

Before any backend deployment is considered complete, provide all of the following:

- Python-compatible container hosting for the FastAPI app
- Managed PostgreSQL with restricted access and tested backup/restore
- Real OIDC provider using authorization-code + PKCE client configuration
- HTTPS/TLS at the edge and between trusted components where required
- Protected secret management for database and identity configuration
- Database migrations run in deployment pipeline and validated
- Health/readiness checks and rollout verification
- CORS policy locked to allowed origins only
- Rate limiting, monitoring, alerting, and incident response basics
- Security and privacy review sign-off

## Authentication and safety prohibitions

Do **not** deploy any environment with:

- `BH_ALLOW_DEV_AUTH=true`
- local development identity headers (for example local-only trusted header impersonation)

Deployment must use production-grade identity verification with real token validation.

## Required provider-specific inputs before backend launch

Backend deployment cannot be finished until a real live backend URL and provider-specific configuration are supplied, including:

- hosting platform service URL(s)
- managed PostgreSQL connection details
- OIDC issuer/audience/JWKS configuration
- production CORS origin list
- secret references in the target environment
