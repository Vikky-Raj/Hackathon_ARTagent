# Note: build this image from the root of the project directory

# Use Python 3.11 as specified in requirements
FROM python:3.11-slim-bookworm

# Update packages to mitigate vulnerabilities
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8010

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install system dependencies and Python packages
# Use a virtual environment to isolate dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        portaudio19-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir psycopg2-binary

# Copy the application code into the container
COPY ./apps /app/apps
COPY ./src /app/src
COPY ./utils /app/utils

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH="/app:$PYTHONPATH"

# Change ownership of the /app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on (configurable via PORT env var)
EXPOSE 8010

# Define the command to run the application
# Port is now configurable via PORT environment variable
CMD uvicorn apps.rtagent.backend.main:app --host 0.0.0.0 --port ${PORT}