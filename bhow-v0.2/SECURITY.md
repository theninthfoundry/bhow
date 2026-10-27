# Security and support boundaries

This is a prototype, **not** a production-vetted medical application. The ingredient data is an educational preview and not clinically reviewed.

`BH_ALLOW_DEV_AUTH=true` and `BH_APP_ENV=local` permit the `X-Dev-User` header from **loopback ASGI peers only**; all other peers receive HTTP 403. **Bind uvicorn to 127.0.0.1 only.** A reverse proxy can make an internet client appear to be a loopback peer; never put local auth behind such a proxy. Do not use personal or real customer records with demo auth.

For staging/production, use OIDC with properly verified token issuer, audience, expiration and keys; disable dev auth, require PostgreSQL, HTTPS and a fully configured privacy lifecycle. Device login and token revocation have not been implemented.

Report suspected vulnerabilities privately to the repository owner. Do not share actual account credentials or sensitive veterinary documents.
