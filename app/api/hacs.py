"""HACS API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
import logging
import aiohttp
import zipfile
import io
import os
from pathlib import Path

from app.models.schemas import Response
from app.services.ha_client import ha_client
from app.main import verify_token

router = APIRouter()
logger = logging.getLogger('ha_cursor_agent')

HACS_GITHUB_REPO = "hacs/integration"
HACS_INSTALL_PATH = "/config/custom_components/hacs"


@router.post("/install", response_model=Response, dependencies=[Depends(verify_token)])
async def install_hacs():
    """
    Install HACS (Home Assistant Community Store)
    
    This will:
    1. Download latest HACS release from GitHub
    2. Extract to custom_components/hacs
    3. Restart Home Assistant
    
    **⚠️ Note:** Home Assistant will restart automatically after installation
    """
    try:
        logger.info("Starting HACS installation...")
        
        # Check if HACS already installed
        hacs_path = Path(HACS_INSTALL_PATH)
        if hacs_path.exists():
            logger.info("HACS is already installed")
            return Response(
                success=True,
                message="HACS is already installed",
                data={"version": "unknown", "path": HACS_INSTALL_PATH}
            )
        
        # Get latest HACS release from GitHub
        logger.info(f"Fetching latest HACS release from GitHub: {HACS_GITHUB_REPO}")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.github.com/repos/{HACS_GITHUB_REPO}/releases/latest") as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=500, detail="Failed to fetch HACS release info")
                release_data = await resp.json()
        
        version = release_data.get("tag_name", "unknown")
        download_url = None
        
        # Find the ZIP asset
        for asset in release_data.get("assets", []):
            if asset["name"] == "hacs.zip":
                download_url = asset["browser_download_url"]
                break
        
        if not download_url:
            raise HTTPException(status_code=500, detail="HACS download URL not found")
        
        logger.info(f"Downloading HACS {version} from {download_url}")
        
        # Download HACS ZIP
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=500, detail="Failed to download HACS")
                zip_content = await resp.read()
        
        logger.info(f"Downloaded {len(zip_content)} bytes")
        
        # Extract ZIP to custom_components/hacs
        logger.info(f"Extracting HACS to {HACS_INSTALL_PATH}")
        os.makedirs(HACS_INSTALL_PATH, exist_ok=True)
        
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
            zip_file.extractall(HACS_INSTALL_PATH)
        
        logger.info("HACS extracted successfully")
        
        # Restart Home Assistant
        logger.warning("Restarting Home Assistant to load HACS...")
        try:
            await ha_client.restart()
        except Exception as restart_error:
            logger.warning(f"Restart command sent, but got error (this is normal): {restart_error}")
        
        return Response(
            success=True,
            message=f"HACS {version} installed successfully. Home Assistant is restarting...",
            data={
                "version": version,
                "path": HACS_INSTALL_PATH,
                "restart_initiated": True
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to install HACS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=Response, dependencies=[Depends(verify_token)])
async def get_hacs_status():
    """
    Check if HACS is installed and get version info
    """
    try:
        hacs_path = Path(HACS_INSTALL_PATH)
        
        if not hacs_path.exists():
            return Response(
                success=True,
                message="HACS is not installed",
                data={
                    "installed": False,
                    "path": HACS_INSTALL_PATH
                }
            )
        
        # Try to read version from manifest
        manifest_path = hacs_path / "manifest.json"
        version = "unknown"
        
        if manifest_path.exists():
            import json
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                version = manifest.get("version", "unknown")
        
        return Response(
            success=True,
            message="HACS is installed",
            data={
                "installed": True,
                "version": version,
                "path": HACS_INSTALL_PATH
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to check HACS status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repositories", response_model=Response, dependencies=[Depends(verify_token)])
async def list_hacs_repositories():
    """
    List HACS repositories (integrations, themes, plugins)
    
    **Note:** This requires HACS to be installed and Home Assistant restarted.
    HACS must be configured via UI first.
    """
    try:
        logger.info("Listing HACS repositories...")
        
        # Check if HACS is installed
        hacs_path = Path(HACS_INSTALL_PATH)
        if not hacs_path.exists():
            raise HTTPException(
                status_code=400, 
                detail="HACS is not installed. Please install HACS first using /api/hacs/install"
            )
        
        # Try to get HACS data via Home Assistant websocket API
        # This is a placeholder - actual implementation would use HA WebSocket API
        # to call HACS services
        
        return Response(
            success=True,
            message="HACS repositories list",
            data={
                "note": "Repository listing requires HACS WebSocket API integration",
                "status": "not_yet_implemented",
                "next_steps": [
                    "Configure HACS in Home Assistant UI",
                    "HACS will then be accessible via HA services"
                ]
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to list HACS repositories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/install_repository", response_model=Response, dependencies=[Depends(verify_token)])
async def install_hacs_repository(repository: str, category: str = "integration"):
    """
    Install a repository from HACS
    
    **Parameters:**
    - repository: Repository name (e.g., "hacs/integration")
    - category: Type of repository (integration, theme, plugin)
    
    **Note:** This requires HACS to be fully configured.
    """
    try:
        logger.info(f"Installing HACS repository: {repository} (category: {category})")
        
        # Check if HACS is installed
        hacs_path = Path(HACS_INSTALL_PATH)
        if not hacs_path.exists():
            raise HTTPException(
                status_code=400,
                detail="HACS is not installed. Please install HACS first."
            )
        
        # This would use HACS services via Home Assistant
        # Placeholder for now
        
        return Response(
            success=True,
            message=f"Repository installation initiated: {repository}",
            data={
                "repository": repository,
                "category": category,
                "status": "not_yet_implemented",
                "note": "Requires HACS WebSocket API integration"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to install HACS repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))

