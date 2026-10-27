# Contributing to Bhow

1. Open an issue with the user job, evidence, acceptance criteria and safety assessment.
2. Keep pure logic in `bhow_core`, storage/API in `bhow_api`, and sources in `bhow_kb`.
3. Write failing tests for bugs; include cross-user authorization cases for all new dog-scoped routes.
4. Run `ruff check src tests`, `ruff format src tests` before committing, `pytest -q`, and migrate up/down locally.
5. Never turn an unreviewed reference into a clinical claim; changes to knowledge-base labels require source/reviewer and version update.
6. Do not commit real personal records, secrets, live pet photos or third-party unlicensed assets.
7. PR description: What changed? How tested? What remains unavailable? Can it be rolled back safely?
