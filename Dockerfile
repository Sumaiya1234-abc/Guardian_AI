# ============================================================================
# Dockerfile for GuardianAI Fraud Detection Environment
# ============================================================================
# Production-ready Docker image for deployment on Hugging Face Spaces
# Includes gymnasium RL environment and web interface
#
# Build: docker build -t guardianai-fraud-detection .
# Run:   docker run -p 7860:7860 guardianai-fraud-detection
# ============================================================================

# Base image: Python 3.10 slim for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    curl \
    ca-certificates \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .
COPY requirements-deployments.txt . 2>/dev/null || true

# Install Python dependencies
RUN pip install -r requirements.txt

# Install additional dependencies for web deployment (if available)
RUN if [ -f requirements-deployments.txt ]; then \
    pip install -r requirements-deployments.txt; \
    else \
    pip install gradio==4.27.0 \
    huggingface-hub==0.21.0 \
    plotly==5.18.0; \
    fi

# Copy application code
COPY . .

# Create directories for data/models if they don't exist
RUN mkdir -p /app/data /app/models /app/logs

# Expose port for Gradio/Streamlit
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Set default command to run the Gradio app
CMD ["python", "app.py"]

# ============================================================================
# Alternative: Multi-stage build for optimized production image
# Uncomment below to use multi-stage build strategy
# ============================================================================
# FROM python:3.10-slim as builder
# WORKDIR /app
# 
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential git && rm -rf /var/lib/apt/lists/*
# 
# COPY requirements.txt .
# RUN pip install --user --no-cache-dir -r requirements.txt
# 
# FROM python:3.10-slim
# WORKDIR /app
# ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
# 
# COPY --from=builder /root/.local /root/.local
# ENV PATH=/root/.local/bin:$PATH
# 
# COPY . .
# EXPOSE 7860
# CMD ["python", "app.py"]

# ============================================================================
# Development Dockerfile variant
# ============================================================================
# For development, use:
# FROM python:3.10
# WORKDIR /app
# RUN apt-get update && apt-get install -y build-essential git
# COPY requirements.txt requirements-dev.txt* ./
# RUN pip install -r requirements.txt && \
#     if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
# COPY . .
# CMD ["bash"]
