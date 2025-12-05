"""
Home Assistant MCP Server - FastAPI Application
Enables AI clients to manage Home Assistant via MCP protocol
"""
import os
import logging
import secrets
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import files, entities, helpers, automations, scripts, system, backup, logs, logbook, ai_instructions, hacs, lovelace, themes
from app.utils.logger import setup_logger
from app.services import ha_websocket
from app.auth import verify_token, set_api_key, security

# Setup logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info').upper()
logger = setup_logger('ha_mcp_server', LOG_LEVEL)

# Server version
SERVER_VERSION = "3.0.0"

# FastAPI app
app = FastAPI(
    title="Home Assistant MCP Server API",
    description="MCP Server for Home Assistant - enables AI clients to manage HA configuration via Model Context Protocol",
    version=SERVER_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track MCP client versions (to avoid logging on every request)
mcp_clients_logged = set()

# Middleware to log MCP client version
@app.middleware("http")
async def log_mcp_client_version(request: Request, call_next):
    """Log MCP client version on first request"""
    mcp_version = request.headers.get('x-mcp-client-version')
    client_id = request.client.host if request.client else 'unknown'
    
    # Log only once per client
    if mcp_version and client_id not in mcp_clients_logged:
        mcp_clients_logged.add(client_id)
        logger.info(f"🔌 MCP Client connected: v{mcp_version} from {client_id}")
    
    response = await call_next(request)
    return response

# Get configuration from environment
HA_TOKEN = os.getenv('HA_TOKEN', '')  # Home Assistant Long-Lived Access Token
HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')

# API Key configuration for MCP clients
API_KEY_FROM_ENV = os.getenv('HA_AGENT_KEY', '').strip()
API_KEY_FILE = Path('/config/.ha_mcp_server_key')

# Global variable for API key
API_KEY = None


def get_or_generate_api_key():
    """
    Get or generate API key for MCP client authentication.
    
    Priority:
    1. API key from environment (HA_AGENT_KEY)
    2. Existing API key from file
    3. Generate new API key and save to file
    """
    # 1. Check environment variable
    if API_KEY_FROM_ENV:
        logger.info("✅ Using API key from environment variable (HA_AGENT_KEY)")
        return API_KEY_FROM_ENV
    
    # 2. Check file
    if API_KEY_FILE.exists():
        api_key = API_KEY_FILE.read_text().strip()
        logger.info("✅ Using existing API key from file")
        return api_key
    
    # 3. Generate new
    api_key = secrets.token_urlsafe(32)  # 256 bits of entropy
    
    try:
        API_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        API_KEY_FILE.write_text(api_key)
        logger.info(f"💾 API key saved to {API_KEY_FILE}")
    except Exception as e:
        logger.warning(f"Failed to save API key to file: {e}")
    
    # Log the key
    logger.info("=" * 70)
    logger.info("🔑 NEW API KEY GENERATED")
    logger.info("=" * 70)
    logger.info(f"API Key: {api_key}")
    logger.info("")
    logger.info("📋 Add this to your MCP client configuration:")
    logger.info('  "env": {')
    logger.info(f'    "HA_AGENT_KEY": "{api_key}"')
    logger.info('  }')
    logger.info("=" * 70)
    
    return api_key


# Initialize API key
API_KEY = get_or_generate_api_key()
set_api_key(API_KEY)  # Set API key in auth module

# Log startup configuration
ha_token_status = "PRESENT" if HA_TOKEN else "MISSING"

logger.info(f"=================================")
logger.info(f"Home Assistant MCP Server v{SERVER_VERSION}")
logger.info(f"=================================")
logger.info(f"HA_TOKEN: {ha_token_status}")
if not HA_TOKEN:
    logger.warning("⚠️  WARNING: No HA_TOKEN configured! Set HA_TOKEN environment variable.")
logger.info(f"HA_URL: {HA_URL}")
logger.info(f"API Key: {'From Environment' if API_KEY_FROM_ENV else 'Auto-generated'}")
logger.info(f"=================================")


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize WebSocket client on startup"""
    if HA_TOKEN:
        logger.info("Initializing WebSocket client...")
        ha_websocket.ha_ws_client = ha_websocket.HAWebSocketClient(
            url=HA_URL,
            token=HA_TOKEN
        )
        await ha_websocket.ha_ws_client.start()
        logger.info("✅ WebSocket client started in background")
    else:
        logger.warning("⚠️ WebSocket client disabled (no HA_TOKEN configured)")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop WebSocket client on shutdown"""
    if ha_websocket.ha_ws_client:
        logger.info("Stopping WebSocket client...")
        await ha_websocket.ha_ws_client.stop()
        logger.info("✅ WebSocket client stopped")


# Include routers
app.include_router(files.router, prefix="/api/files", tags=["Files"], dependencies=[Depends(verify_token)])
app.include_router(entities.router, prefix="/api/entities", tags=["Entities"], dependencies=[Depends(verify_token)])
app.include_router(helpers.router, prefix="/api/helpers", tags=["Helpers"], dependencies=[Depends(verify_token)])
app.include_router(automations.router, prefix="/api/automations", tags=["Automations"], dependencies=[Depends(verify_token)])
app.include_router(scripts.router, prefix="/api/scripts", tags=["Scripts"], dependencies=[Depends(verify_token)])
app.include_router(system.router, prefix="/api/system", tags=["System"], dependencies=[Depends(verify_token)])
app.include_router(backup.router, prefix="/api/backup", tags=["Backup"], dependencies=[Depends(verify_token)])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"], dependencies=[Depends(verify_token)])
app.include_router(logbook.router, prefix="/api/logbook", tags=["Logbook"], dependencies=[Depends(verify_token)])
app.include_router(hacs.router, prefix="/api/hacs", tags=["HACS"])
app.include_router(lovelace.router, prefix="/api/lovelace", tags=["Lovelace"], dependencies=[Depends(verify_token)])
app.include_router(themes.router, prefix="/api/themes", tags=["Themes"], dependencies=[Depends(verify_token)])
app.include_router(ai_instructions.router, prefix="/api/ai")


@app.get("/")
async def root():
    """Root endpoint - server information"""
    return {
        "name": "Home Assistant MCP Server",
        "version": SERVER_VERSION,
        "status": "running",
        "ha_url": HA_URL,
        "ha_connected": bool(HA_TOKEN),
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health():
    """Health check endpoint (no auth required)"""
    return {
        "status": "healthy",
        "version": SERVER_VERSION,
        "config_path": os.getenv('CONFIG_PATH', '/config'),
        "git_enabled": os.getenv('ENABLE_GIT', 'false') == 'true',
        "ha_url": HA_URL,
        "ha_token_configured": bool(HA_TOKEN)
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8099))
    uvicorn.run(app, host="0.0.0.0", port=port)
