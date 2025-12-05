# Migration Guide: From HA Cursor Agent Add-on to Standalone MCP Server

This document explains the changes made to convert the original Home Assistant Cursor Agent add-on into a standalone MCP server.

---

## Overview of Changes

### What Was Removed

1. **Home Assistant OS Add-on Dependencies:**
   - Removed `config.yaml` (add-on configuration)
   - Removed `build.json` (add-on build config)
   - Removed `repository.json` (add-on repository metadata)
   - Removed Supervisor API client (`app/services/supervisor_client.py`)
   - Removed add-on management endpoints (`app/api/addons.py`)
   - Removed ingress panel functionality

2. **Documentation:**
   - Removed add-on specific documentation
   - Removed GitHub issue templates
   - Removed test suites specific to add-on operation

3. **Features No Longer Available:**
   - Add-on installation/management (since this is not an add-on)
   - Supervisor API access (only available in HA OS)
   - Ingress panel (HA OS add-on feature)
   - Automatic SUPERVISOR_TOKEN injection

### What Was Changed

1. **Authentication:**
   - **Old:** Used `SUPERVISOR_TOKEN` (auto-provided by HA OS)
   - **New:** Uses `HA_TOKEN` (Long-Lived Access Token you create)

2. **Configuration:**
   - **Old:** Configured through HA OS add-on UI
   - **New:** Configured through `.env` file

3. **Deployment:**
   - **Old:** Installed as Home Assistant add-on
   - **New:** Runs as standalone Docker container

4. **Branding:**
   - **Old:** "HA Cursor Agent" (specific to Cursor AI)
   - **New:** "Home Assistant MCP Server" (works with any MCP client)

5. **Base Docker Image:**
   - **Old:** `ghcr.io/home-assistant/amd64-base-python:3.12-alpine3.20`
   - **New:** `python:3.11-alpine`

---

## Breaking Changes

### For End Users

1. **Installation Method:**
   - Can no longer install through HA OS add-on store
   - Must use Docker Compose or manual Docker deployment

2. **Configuration:**
   - Must manually create Long-Lived Access Token
   - Must set environment variables in `.env` file
   - No UI configuration interface

3. **Network Access:**
   - Must configure `HA_URL` to point to Home Assistant
   - Can't use `http://supervisor/core` (only works in add-ons)
   - Must use actual IP address or hostname

4. **Add-on Management:**
   - Can no longer install/manage HA OS add-ons
   - Feature was specific to Home Assistant OS

### For Developers

1. **API Changes:**
   - Removed `/api/addons/*` endpoints
   - Removed ingress panel endpoints (`/` and `/old`)
   - Health check now returns different information

2. **Authentication:**
   - `SUPERVISOR_TOKEN` no longer available
   - Must use `HA_TOKEN` for all Home Assistant API calls
   - Supervisor client dependency removed

3. **File Structure:**
   - Removed `app/ingress_panel.py`
   - Removed `app/templates/ingress_panel.html`
   - Simplified `app/main.py` significantly

---

## Migration Steps

### If You Were Using the Add-on

1. **Export Your Configuration:**
   - Note your current settings (API key, etc.)
   - Back up any customizations

2. **Create Long-Lived Access Token:**
   - In Home Assistant UI → Profile → Long-Lived Access Tokens
   - Create new token and save it securely

3. **Deploy Standalone Version:**
   ```bash
   # Clone the new repository
   git clone https://github.com/itsmrshow/home-assistant-mcp-server.git
   cd home-assistant-mcp-server
   
   # Configure
   cp .env.example .env
   # Edit .env with your HA_URL and HA_TOKEN
   
   # Start
   docker-compose up -d
   ```

4. **Update MCP Client Configuration:**
   - Change URL from `http://homeassistant.local:8099` if needed
   - Update API key if it was regenerated

5. **Test:**
   - Verify health endpoint: `curl http://localhost:8099/api/health`
   - Test with your AI client

6. **Remove Old Add-on:**
   - Uninstall the old HA Cursor Agent add-on from HA OS

### If You Were Developing

1. **Update Dependencies:**
   - Remove any references to `supervisor_client`
   - Update imports in your code
   - Remove `addons` router if you were using it

2. **Update Authentication:**
   - Replace `SUPERVISOR_TOKEN` with `HA_TOKEN`
   - Update API calls to use new token

3. **Update Configuration:**
   - Switch from add-on config to environment variables
   - Update docker-compose or deployment scripts

---

## Feature Comparison

| Feature | Old (Add-on) | New (Standalone) |
|---------|--------------|------------------|
| **Installation** | HA OS Add-on Store | Docker Compose |
| **Configuration** | HA OS UI | .env file |
| **Authentication** | SUPERVISOR_TOKEN (auto) | HA_TOKEN (manual) |
| **Home Assistant Type** | HA OS only | Any (Container, Core, etc.) |
| **AI Client** | Cursor specific | Any MCP client |
| **Add-on Management** | ✅ Yes | ❌ No |
| **HACS Integration** | ✅ Yes | ✅ Yes |
| **File Management** | ✅ Yes | ✅ Yes |
| **Git Versioning** | ✅ Yes | ✅ Yes |
| **Automations/Scripts** | ✅ Yes | ✅ Yes |
| **Entities** | ✅ Yes | ✅ Yes |
| **Ingress Panel** | ✅ Yes | ❌ No |
| **Network Isolation** | HA OS managed | Self-managed |

---

## Advantages of Standalone Version

1. **Works with Any HA Installation:**
   - Container, Core, Supervised, OS - all supported
   - Not limited to Home Assistant OS

2. **Works with Any MCP Client:**
   - Cursor, Claude Desktop, or custom clients
   - Not tied to specific AI tool

3. **Easier Development:**
   - Standard Python/Docker development
   - No add-on build process
   - Faster iteration

4. **More Control:**
   - Choose your own deployment method
   - Configure networking as needed
   - Customize Docker image

5. **Better for Advanced Users:**
   - Full control over environment
   - Can run on separate hardware
   - Easier to scale

---

## Disadvantages vs Add-on

1. **More Manual Setup:**
   - Must create access token manually
   - Must configure environment variables
   - No UI for configuration

2. **No Add-on Management:**
   - Can't install/manage HA OS add-ons
   - Feature only exists in HA OS

3. **No Ingress:**
   - No integrated web UI in HA
   - Must access server directly

4. **Network Configuration:**
   - Must handle networking yourself
   - No automatic supervisor network access

---

## Troubleshooting

### "Connection refused" errors

**Cause:** `HA_URL` is incorrect or Home Assistant is not accessible

**Solution:**
- Verify Home Assistant is running
- Check IP address/hostname in `.env`
- Test with: `curl -H "Authorization: Bearer $HA_TOKEN" $HA_URL/api/`

### "Unauthorized" errors

**Cause:** `HA_TOKEN` is invalid or expired

**Solution:**
- Verify token in Home Assistant UI
- Generate new Long-Lived Access Token
- Update `.env` file
- Restart container

### "Add-on endpoints not found"

**Cause:** Trying to use removed add-on management features

**Solution:**
- These features are not available in standalone version
- Only available in Home Assistant OS add-on mode
- Use Home Assistant UI for add-on management

---

## Support

- **Issues:** https://github.com/itsmrshow/home-assistant-mcp-server/issues
- **Original Project:** https://github.com/Coolver/home-assistant-cursor-agent

---

## Contributing

If you encounter issues with the migration or have suggestions for improvement, please open an issue or pull request!
