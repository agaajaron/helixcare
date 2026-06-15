# CareGraph production image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for llama-cpp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better caching)
COPY docker/requirements.txt /app/docker/requirements.txt
RUN pip install --no-cache-dir -r /app/docker/requirements.txt

# Copy source
COPY app /app/app
COPY data /app/data

# Optional models dir (empty by default - mount at runtime if needed)
RUN mkdir -p /app/models

# Ports: Streamlit UI + Prometheus metrics
EXPOSE 8501 9000

# Environment knobs
ENV LLAMA_CPP_MODEL_PATH=/app/models/YOUR_MODEL.gguf

# Default command runs the Streamlit UI
CMD ["bash","-lc","streamlit run app/ui.py --server.address 0.0.0.0 --server.port 8501"]
