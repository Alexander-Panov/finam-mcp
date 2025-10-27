FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /mcp

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Copy the project into the image
COPY . .
ENV PYTHONPATH=./