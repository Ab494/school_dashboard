# ── Base image ───────────────────────────────────────
# Python 3.11 slim — smaller than full image
FROM python:3.11-slim

# ── Set environment variables ────────────────────────
# PYTHONDONTWRITEBYTECODE — stops Python writing .pyc files (not needed in containers)
# PYTHONUNBUFFERED — forces stdout/stderr to be unbuffered (logs appear immediately)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ── Install system dependencies ──────────────────────
# psycopg2 needs libpq-dev to connect to PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ──────────────────────
# Copy requirements first for Docker layer caching
# If requirements.txt hasn't changed, this step is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project code ────────────────────────────────
COPY . .

# ── Collect static files ─────────────────────────────
# Django needs this to serve CSS/JS/images via WhiteNoise
# Must run before starting the server
RUN python manage.py collectstatic --noinput

# ── Expose port ──────────────────────────────────────
EXPOSE 8000

# ── Start with Gunicorn ──────────────────────────────
# Gunicorn is a production-grade WSGI server
# Never use Django's built-in dev server (manage.py runserver) in production
# --bind 0.0.0.0:8000 — listen on all interfaces
# --workers 2 — 2 worker processes
CMD ["gunicorn", "school_dashboard.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
