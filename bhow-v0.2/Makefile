.PHONY: dev test lint format migrate smoke

dev:
	uvicorn bhow_api.main:app --reload --host 127.0.0.1 --port 8000
migrate:
	alembic upgrade head
test:
	pytest -q
lint:
	ruff check src tests && mypy --strict src/bhow_core
format:
	ruff check --fix src tests && ruff format src tests
smoke:
	python tools/smoke.py
