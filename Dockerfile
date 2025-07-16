# Stage 1: Builder
FROM python:3.13-alpine AS builder

# Install build dependencies for Python packages (one-time only)
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    cargo \
    libxml2-dev \
    libxslt-dev \
    jpeg-dev \
    zlib-dev

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first to cache better
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-alpine

# Install runtime dependencies only
RUN apk add --no-cache \
    libffi \
    libxml2 \
    libxslt \
    jpeg \
    zlib

# Create non-root user using Alpine's adduser
RUN adduser -D -H -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser ./src /app/

# Use non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "pitstop.wsgi:application"]
