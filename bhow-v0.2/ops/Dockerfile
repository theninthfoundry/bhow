FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN pip install --no-cache-dir .
COPY alembic.ini /app/
COPY alembic /app/alembic
RUN adduser --disabled-password --gecos '' --uid 10001 bhow
USER bhow
EXPOSE 8000
CMD ["uvicorn", "bhow_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "127.0.0.1"]
