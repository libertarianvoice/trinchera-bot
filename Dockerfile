# Trinchera Libertaria Bot - Dockerfile (versión ligera SIN base de datos)
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev)
RUN uv sync --frozen --no-dev --no-install-project

# Final stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Make sure we use the virtualenv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

# Copy source (versión ligera sin DB ni migraciones)
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Default command (polling). Override for webhook.
CMD ["python", "-m", "trinchera_bot.main"]

# Healthcheck (optional - implement /health in webhook mode)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1