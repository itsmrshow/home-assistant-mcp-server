# Home Assistant MCP Server - Standalone Docker Image
FROM python:3.11-alpine

# Version: 3.0.0 - Standalone MCP Server (not an add-on)
LABEL maintainer="Home Assistant MCP Server"
LABEL description="MCP Server for Home Assistant - enables AI clients to manage HA via Model Context Protocol"

# Install system dependencies
RUN apk add --no-cache \
    git \
    bash \
    curl \
    jq

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY ./entrypoint.sh ./

# Make script executable
RUN chmod +x entrypoint.sh

# Create config directory
RUN mkdir -p /config

# Expose port
EXPOSE 8099

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8099/api/health || exit 1

# Run
CMD ["./entrypoint.sh"]
