"""Fail closed before staging deployment. Never prints secrets or token contents.

Run from bhow-v0.2: `python tools/preflight.py --check-db` after migrations.
"""
import argparse
import sys

from sqlalchemy import create_engine, text

from bhow_api.config import Settings


def main() -> int:
    parser = argparse.ArgumentParser(description="Bhow staging configuration preflight")
    parser.add_argument("--check-db", action="store_true", help="Check DB connectivity and migrations")
    args = parser.parse_args()
    try:
        settings = Settings()
        if settings.app_env not in {"staging", "production"}:
            raise ValueError("Preflight requires BH_APP_ENV=staging or production")
        print("PASS: deployment settings validated (values withheld)")
        if args.check_db:
            engine = create_engine(settings.database_url, pool_pre_ping=True)
            try:
                with engine.connect() as connection:
                    result = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one_or_none()
                    if result != "0002":
                        raise RuntimeError("Database migration not current; run alembic upgrade head")
                    connection.execute(text("SELECT 1"))
                print("PASS: database reachable, migration 0002 present")
            finally:
                engine.dispose()
        return 0
    except Exception as exc:  # don't print DSN or other raw config in failures
        print(f"FAIL: {type(exc).__name__}; verify sanitized staging settings and migrations", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
