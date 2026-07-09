FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 \
    fonts-dejavu fonts-liberation \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv using the official standalone installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first to leverage Docker caching
COPY pyproject.toml uv.lock* ./

# Install dependencies into the system environment using uv
RUN uv sync --frozen --no-dev --system

# Copy the rest of the application
COPY . .

EXPOSE 8000

# Use uv run to execute your production command safely
CMD uv run --system python manage.py collectstatic --noinput && uv run --system gunicorn config.wsgi:application --bind 0.0.0.0:8000
