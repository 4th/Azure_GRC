# infra/container-images/scorecard-app/Dockerfile
#
# Production container image for the 4th.GRC TrustOps Scorecard (Streamlit app).
# Assumes:
#   - Streamlit entrypoint: apps/scorecard/streamlit_app.py
#   - requirements.txt at repo root

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system deps (add if your libs need more)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install Python deps
COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy application source into the image
COPY . .

# Default Streamlit port
EXPOSE 8501

# Environment variables (can be overridden at deploy time)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Prevent Streamlit from trying to open a browser in container
ENV STREAMLIT_BROWSER_SERVER_ADDRESS=0.0.0.0

# Start the TrustOps Scorecard Streamlit app
CMD ["streamlit", "run", "apps/scorecard/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
