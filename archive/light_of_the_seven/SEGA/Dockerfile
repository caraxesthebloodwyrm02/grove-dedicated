# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Set working directory
WORKDIR /app

# Builder stage: install dependencies in a venv
FROM base AS builder

# Copy packaging files first for better layer caching
COPY --link pyproject.toml README.md ./
COPY --link src/ ./src/

# Create venv and install package (reads deps from pyproject.toml)
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install .

# Copy remaining application code
COPY --link . ./

# Final stage: minimal image with venv and app code, non-root user
FROM base AS final

# Create non-root user and group
RUN addgroup --system sega && adduser --system --ingroup sega sega

WORKDIR /app

# Copy venv and app code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/ /app/

# Set environment to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER sega

# Default command (adjust as needed, e.g., to run orchestrator.py)
CMD ["python", "orchestrator.py"]
