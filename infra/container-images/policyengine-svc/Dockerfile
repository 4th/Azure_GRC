# infra/container-images/policyengine-svc/Dockerfile
#
# Production container image for the 4th.GRC PolicyEngine service.
# Assumes:
#   - FastAPI app at: services.policyengine_svc.main:app
#   - requirements.txt at repo root

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system dependencies (add more if your libs need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install Python deps
# If you use pyproject.toml/poetry instead, swap this section out.
COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy application source into the image
# This copies the whole repo; you can narrow this if desired.
COPY . .

# Expose the port used by uvicorn in container
EXPOSE 8080

# Optional: default log level / config via env
ENV POLICYENGINE_HOST=0.0.0.0
ENV POLICYENGINE_PORT=8080

# Start the FastAPI PolicyEngine service
CMD ["uvicorn", "services.policyengine_svc.main:app", "--host", "0.0.0.0", "--port", "8080"]
