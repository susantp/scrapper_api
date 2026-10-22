
# Build dependencies
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=0

WORKDIR /app

COPY requirements.txt .

RUN uv venv /opt/venv && \
    uv pip install \
        --python /opt/venv/bin/python \
        --no-cache \
        -r requirements.txt

# Lightweight production image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_NAME="fast api"

WORKDIR /var/www/fastApi

COPY --from=builder /opt/venv /opt/venv

COPY . .

# Run as non-root
RUN useradd --create-home --uid 10001 appuser && \
    chown -R appuser:appuser /var/www/fastApi

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
