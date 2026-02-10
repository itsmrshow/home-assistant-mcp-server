"""
Authentication and authorization utilities
"""
import os
import logging
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.env import load_env
load_env()

logger = logging.getLogger('ha_cursor_agent')

# Security
security = HTTPBearer()

# Get tokens from environment
SUPERVISOR_TOKEN = os.getenv('SUPERVISOR_TOKEN', '')  # Auto-provided by HA when running as add-on
DEV_TOKEN = os.getenv('HA_AGENT_KEY', '')  # For local development only

# Global variable for API key (will be set by main.py)
API_KEY = None


def set_api_key(key: str):
    """Set the API key (called from main.py)"""
    global API_KEY
    API_KEY = key


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify API key.

    Validates the Bearer token against the API_KEY set by main.py.
    This works for both add-on mode and standalone Docker mode.

    Add-on mode: SUPERVISOR_TOKEN is used internally for HA API operations.
    Standalone mode: HA_TOKEN is used internally for HA API operations.
    In both cases, the MCP client authenticates with the API_KEY.
    """
    token = credentials.credentials
    token_preview = f"{token[:20]}..." if len(token) > 20 else token

    # Always validate against API_KEY (set by main.py on startup)
    if API_KEY and token == API_KEY:
        logger.debug(f"API key validated: {token_preview}")
        return token

    # Fallback: check DEV_TOKEN for backwards compatibility
    if DEV_TOKEN and token == DEV_TOKEN:
        logger.debug(f"Token validated via HA_AGENT_KEY")
        return token

    logger.warning(f"Invalid API key: {token_preview}")
    raise HTTPException(status_code=401, detail="Invalid API key")


