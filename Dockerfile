# Build stage
FROM python:3.12-alpine AS builder

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Clean up build dependencies
RUN apk del .build-deps

# Production stage
FROM python:3.12-alpine

# Install runtime dependencies only
RUN apk add --no-cache --virtual .runtime-deps \
    curl \
    && rm -rf /var/cache/apk/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create app user with specific UID/GID for better security
RUN addgroup -g 1001 app && \
    adduser -D -s /bin/sh -u 1001 -G app app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=app:app app.py .

# Switch to app user
USER app

# Expose port
EXPOSE 8080

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run application
CMD ["python", "app.py"] 