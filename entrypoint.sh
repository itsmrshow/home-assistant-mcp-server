#!/bin/sh

# Initialize Git repo if enabled
if [ "$ENABLE_GIT" = "true" ]; then
    echo "Initializing Git repository for config versioning..."
    cd /config
    if [ ! -d ".git" ]; then
        git init
        git config user.name "HA MCP Server"
        git config user.email "mcp@homeassistant.local"
        git add -A
        git commit -m "Initial commit by HA MCP Server" || true
        echo "Git repository initialized"
    fi
    cd /app
fi

echo "Starting Home Assistant MCP Server on port $PORT..."
echo "Log level: $LOG_LEVEL"
echo "Git versioning: $ENABLE_GIT"
echo "Auto backup: $AUTO_BACKUP"

# Start FastAPI application
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --log-level "$LOG_LEVEL"