# Bhow v0.2 — Flet care-journal client

Four functional tabs: **Today** (overview and tasks), **Passport** (timeline and caregiver notes), **Check** (limited text-based hazard flags), **Explore** (explicitly offline educational references). Welcome and multiple-dog switcher are functional against FastAPI.

## Local launch

From the repository root, start the API with `.env` set for local development:

```bash
python -m pip install -e '.[dev]'
alembic upgrade head
uvicorn bhow_api.main:app --reload
```

In a second terminal, install Flet in an environment with network access:

```bash
cd client
python -m pip install -e .
# macOS / Linux
export BH_CLIENT_DEV_AUTH=true
export BH_API_URL=http://127.0.0.1:8000
python main.py
```

On Windows PowerShell, use `$env:BH_CLIENT_DEV_AUTH='true'` and `$env:BH_API_URL='http://127.0.0.1:8000'`. On Android emulator, use `adb reverse tcp:8000 tcp:8000` if connecting to a local development API; **do not** allow preview identity headers on any internet-facing deployment.

## Limitations

- Runtime check on Flet could not be performed in the authoring environment because the Flet package could not be downloaded; API integration and client state tests do run locally. See `docs/29_CLIENT_MILESTONE.md`.
- The UI operates synchronously on network calls; after user testing, move network actions to nonblocking tasks and add optimistic loading states before shipping.
- No persistent mobile OIDC login, secure token vault, dog photos, maps, breed ML, real-time alerts, push notifications, or veterinarian verification are included.
- No claim that a caregiver-entered task is an official vaccination schedule. All safety information is educational and not a substitute for a veterinarian.

Icons are built into Flet; no stock photos or generated illustrations were included.
