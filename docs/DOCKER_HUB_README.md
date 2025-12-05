# Home Assistant MCP Server

**A standalone MCP (Model Context Protocol) server that enables AI assistants to interact with Home Assistant** 🏠🤖

[![GitHub](https://img.shields.io/badge/GitHub-itsmrshow%2Fhome--assistant--mcp--server-blue?logo=github)](https://github.com/itsmrshow/home-assistant-mcp-server)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/itsmrshow/home-assistant-mcp-server)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/itsmrshow/home-assistant-mcp-server/blob/main/LICENSE)

## What is this?

Home Assistant MCP Server is a FastAPI-based REST API server that bridges AI assistants with Home Assistant through the Model Context Protocol. It works with **any** Home Assistant installation (Container, Core, Supervised, or OS) and **any** MCP-compatible AI client (Cursor, Claude Desktop, etc.).

## ⚡ Quick Start

```yaml
services:
  ha-mcp-server:
    image: itsmrshow/home-assistant-mcp-server:latest
    container_name: ha-mcp-server
    ports:
      - "8099:8099"
    volumes:
      - ./config:/config:rw
    environment:
      - HA_URL=http://YOUR_HOME_ASSISTANT_IP:8123
      - HA_TOKEN=your_long_lived_access_token_here
      - ENABLE_GIT=true
      - AUTO_BACKUP=true
    restart: unless-stopped
```

Start it:
```bash
docker-compose up -d
```

**The server automatically generates configuration files in `config/`:**
- `MCP_CLIENT_SETUP.md` - Complete setup instructions
- `mcp_client_config.json` - Ready-to-use MCP client configuration with your API key

Just copy the contents from `mcp_client_config.json` into your AI client's config file!

## 🌟 Key Features

- **🏠 Full Home Assistant Integration** - List entities, call services, monitor states, reload components
- **📦 HACS Management** - Install and manage custom integrations, themes, and plugins
- **🔧 Component Management** - Create/delete automations, scripts, and input helpers
- **📁 Safe File Operations** - Automatic backups before modifications with YAML validation
- **💾 Git Versioning** - Auto-commit every change with rollback capability (up to 50 commits)
- **📊 Monitoring** - Server logs, operation history, and health check endpoints
- **🔒 Secure** - API key authentication with Home Assistant token integration
- **⚡ Auto-Configuration** - Generates MCP client config files automatically on startup

## 🤖 What AI Can Do

- **Analyze** your entire HA setup (entities, automations, scripts, helpers)
- **Build** complete automation systems and Lovelace dashboards
- **Deploy** optimized scripts based on your devices
- **Manage** HACS integrations and community themes
- **Safe Operations** with automatic git versioning and configuration validation

## 🚀 Getting Started

### 1. Get Your Home Assistant Token

1. Open your Home Assistant UI
2. Go to your profile (click your username in the sidebar)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Give it a name (e.g., "MCP Server")
6. Copy the token

### 2. Start the Server

Create `docker-compose.yml` with the configuration above, then:
```bash
docker-compose up -d
```

### 3. Get Your MCP Client Configuration

```bash
# View the setup instructions
cat config/MCP_CLIENT_SETUP.md

# Or get the config directly
cat config/mcp_client_config.json
```

### 4. Configure Your AI Client

**For Cursor:** Copy `config/mcp_client_config.json` contents to `~/.cursor/mcp.json`

**For Claude Desktop:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Restart your AI client and test with: **"List my Home Assistant entities"**

## 🖥️ Supported Platforms

- `linux/amd64` (Intel/AMD 64-bit)
- `linux/arm64` (ARM 64-bit - Raspberry Pi 4, Apple Silicon, etc.)

## ⚙️ Configuration

**Required environment variables:**
- `HA_URL` - Your Home Assistant URL (e.g., `http://192.168.1.100:8123`)
- `HA_TOKEN` - Long-Lived Access Token from Home Assistant

**Optional variables:**
- `PORT` - Server port (default: 8099)
- `LOG_LEVEL` - Logging level (default: info)
- `ENABLE_GIT` - Enable git versioning (default: true)
- `AUTO_BACKUP` - Auto backup on changes (default: true)
- `MAX_BACKUPS` - Maximum git commits (default: 50)
- `CONFIG_PATH` - Config storage path (default: /config)
- `MCP_SERVER_URL` - Server URL for client config (default: http://localhost:8099)

## 📚 API Endpoints

- **Entities:** List, get states, call services
- **Automations:** Create, list, delete automations
- **Scripts:** Create, list, delete scripts
- **Helpers:** Create input_boolean, input_text, input_number, etc.
- **Files:** Read, write, list, delete configuration files
- **HACS:** Install HACS, search repositories, install integrations
- **System:** Reload components, validate config, get system info
- **Backup:** Git history, rollback, view diffs
- **Lovelace:** Manage dashboards and UI configurations
- **Themes:** Install and manage themes

**API Documentation:**
- Swagger UI: `http://localhost:8099/docs`
- ReDoc: `http://localhost:8099/redoc`
- Health Check: `http://localhost:8099/api/health`

## 🔧 Troubleshooting

**Server won't start?**
```bash
# Check logs
docker-compose logs -f

# Verify environment variables
docker-compose config
```

**Can't connect to Home Assistant?**
```bash
# Test connection
curl -H "Authorization: Bearer YOUR_TOKEN" http://YOUR_HA_IP:8123/api/
```

**MCP client can't connect?**
```bash
# Verify server is running
docker-compose ps

# Check API key
cat config/.ha_mcp_server_key

# Test API
curl http://localhost:8099/api/health
```

**Need to access from another machine?**
- Set `MCP_SERVER_URL=http://YOUR_SERVER_IP:8099` in environment variables
- This updates the generated client config with the correct URL

## 🔒 Security Best Practices

1. Never commit `.env` files or tokens to git
2. Run on a trusted network only
3. Keep your `HA_AGENT_KEY` secret
4. Use strong Long-Lived Access Tokens
5. Consider using a reverse proxy with HTTPS for production
6. Rotate tokens periodically

## 📖 Documentation

- **Full Documentation:** [GitHub README](https://github.com/itsmrshow/home-assistant-mcp-server)
- **Setup Guide:** [Quick Start](https://github.com/itsmrshow/home-assistant-mcp-server#-quick-start)
- **API Reference:** Available at `http://localhost:8099/docs` after starting

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/itsmrshow/home-assistant-mcp-server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/itsmrshow/home-assistant-mcp-server/discussions)

## 📝 Version

**Current: 3.0.0** - Standalone Docker MCP Server

### What's New in 3.0.0
- 🐳 Converted to standalone Docker container
- 🏠 Support for any Home Assistant installation type
- 🤖 Compatible with any MCP-enabled AI client
- ⚡ Auto-generates MCP client configuration files
- 💾 Built-in git versioning with rollback
- 🔒 Simplified authentication using HA tokens

## 📄 License

MIT License - See [LICENSE](https://github.com/itsmrshow/home-assistant-mcp-server/blob/main/LICENSE)

## 🙏 Acknowledgments

Forked from [home-assistant-cursor-agent](https://github.com/Coolver/home-assistant-cursor-agent) by Coolver

---

**Made with ❤️ for the Home Assistant and AI community**
