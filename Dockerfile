# ==========================================
# Stage 1: Build Dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Copy dependency specifications
COPY requirements.txt .

# Install dependencies into user site-packages for clean multi-stage transfer
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Minimal Runtime Environment
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Install curl for health check probe and diagnostics
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Ensure local Python binary path is available
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    APP_PORT=8000 \
    APP_ENV=production

# Copy application source code
COPY app/ ./app/

# Expose configured application port
EXPOSE 8000

# Container healthcheck using the /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${APP_PORT}/health || exit 1

# Run the FastAPI application with Uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}"]
