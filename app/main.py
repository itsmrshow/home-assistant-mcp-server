"""
HA Cursor Agent - FastAPI Application
Enables Cursor AI to manage Home Assistant configuration
"""
import os
import logging
import aiohttp
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import files, entities, helpers, automations, scripts, system, backup, logs, ai_instructions
from app.utils.logger import setup_logger

# Setup logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info').upper()
logger = setup_logger('ha_cursor_agent', LOG_LEVEL)

# FastAPI app
app = FastAPI(
    title="HA Cursor Agent API",
    description="AI Agent API for Home Assistant - enables Cursor AI to manage HA configuration",
    version="1.0.2",
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

# Security
security = HTTPBearer()

# Get tokens from environment
SUPERVISOR_TOKEN = os.getenv('SUPERVISOR_TOKEN', '')  # Auto-provided by HA when running as add-on
DEV_TOKEN = os.getenv('HA_TOKEN', '')  # For local development only
HA_URL = os.getenv('HA_URL', 'http://supervisor/core')

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify API token by validating it against Home Assistant API.
    
    Add-on mode (SUPERVISOR_TOKEN exists):
    - Validates user's Long-Lived Access Token by making test request to HA API
    - If token is valid in HA, grants access to agent
    - Agent uses SUPERVISOR_TOKEN internally for privileged operations
    
    Development mode (no SUPERVISOR_TOKEN):
    - Validates against DEV_TOKEN environment variable
    """
    token = credentials.credentials
    
    if SUPERVISOR_TOKEN:
        # Add-on mode: validate token against HA API
        try:
            async with aiohttp.ClientSession() as session:
                # Test token by calling HA API
                async with session.get(
                    f"{HA_URL}/api/",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.debug(f"Token validated successfully")
                        return token
                    else:
                        logger.warning(f"Invalid token: HA API returned {response.status}")
                        raise HTTPException(status_code=401, detail="Invalid Home Assistant token")
        except aiohttp.ClientError as e:
            logger.error(f"Failed to validate token: {e}")
            raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(status_code=401, detail="Token validation failed")
    else:
        # Development mode: strict token check
        if not DEV_TOKEN or token != DEV_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return token

# Include routers
app.include_router(files.router, prefix="/api/files", tags=["Files"], dependencies=[Depends(verify_token)])
app.include_router(entities.router, prefix="/api/entities", tags=["Entities"], dependencies=[Depends(verify_token)])
app.include_router(helpers.router, prefix="/api/helpers", tags=["Helpers"], dependencies=[Depends(verify_token)])
app.include_router(automations.router, prefix="/api/automations", tags=["Automations"], dependencies=[Depends(verify_token)])
app.include_router(scripts.router, prefix="/api/scripts", tags=["Scripts"], dependencies=[Depends(verify_token)])
app.include_router(system.router, prefix="/api/system", tags=["System"], dependencies=[Depends(verify_token)])
app.include_router(backup.router, prefix="/api/backup", tags=["Backup"], dependencies=[Depends(verify_token)])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"], dependencies=[Depends(verify_token)])
app.include_router(ai_instructions.router, prefix="/api/ai")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "HA Cursor Agent API",
        "version": "1.0.2",
        "description": "AI Agent API for Home Assistant",
        "docs": "/docs",
        "ai_instructions": "/api/ai/instructions",
        "endpoints": {
            "files": "/api/files",
            "entities": "/api/entities",
            "helpers": "/api/helpers",
            "automations": "/api/automations",
            "scripts": "/api/scripts",
            "system": "/api/system",
            "backup": "/api/backup",
            "logs": "/api/logs",
            "ai": "/api/ai/instructions"
        }
    }

@app.get("/api/health")
async def health():
    """Health check endpoint (no auth required)"""
    return {
        "status": "healthy",
        "version": "1.0.2",
        "config_path": os.getenv('CONFIG_PATH', '/config'),
        "git_enabled": os.getenv('ENABLE_GIT', 'false') == 'true',
        "ai_instructions": "/api/ai/instructions"
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

