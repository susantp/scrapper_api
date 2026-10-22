
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /bin/uv

# Build tools only in builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV UV_PYTHON_DOWNLOADS=0 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


# Lightweight production image
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    APP_NAME="fast api"

WORKDIR /app

RUN useradd --uid 10001 --no-create-home appuser

COPY --from=builder --chown=10001:10001 /app /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4"]
