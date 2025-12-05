# Docker Publishing Guide

This document explains how Docker images are automatically built and published for this project.

---

## Automated Publishing

The project uses GitHub Actions to automatically build and publish Docker images to:

1. **Docker Hub:** `itsmrshow/home-assistant-mcp-server`
2. **GitHub Container Registry (GHCR):** `ghcr.io/itsmrshow/home-assistant-mcp-server`

### Supported Platforms

Multi-architecture images are built for:
- `linux/amd64` - Intel/AMD 64-bit processors
- `linux/arm64` - ARM 64-bit (Raspberry Pi 4, Apple Silicon, etc.)
- `linux/arm/v7` - ARM 32-bit (Raspberry Pi 3, etc.)

---

## When Images Are Built

Images are automatically built and published when:

1. **Push to main branch** - Creates `:latest` tag
2. **Version tags** (e.g., `v3.0.0`) - Creates version-specific tags:
   - `:3.0.0` (full version)
   - `:3.0` (minor version)
   - `:3` (major version)
   - `:latest` (if on main branch)
3. **Manual trigger** - Via GitHub Actions workflow dispatch

---

## Setting Up Docker Hub Publishing

To enable Docker Hub publishing, you need to configure GitHub secrets:

### 1. Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Log in to your account
3. Click your username → **Account Settings**
4. Go to **Security** → **Access Tokens**
5. Click **New Access Token**
6. Give it a description (e.g., "GitHub Actions - home-assistant-mcp-server")
7. Set permissions to **Read & Write**
8. Click **Generate**
9. **Copy the token** (you won't see it again!)

### 2. Add Secrets to GitHub Repository

1. Go to your GitHub repository: https://github.com/itsmrshow/home-assistant-mcp-server
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these two secrets:

**Secret 1:**
- Name: `DOCKER_USERNAME`
- Value: Your Docker Hub username (e.g., `itsmrshow`)

**Secret 2:**
- Name: `DOCKER_PASSWORD`
- Value: The access token you generated in step 1

### 3. Verify Setup

The GitHub Actions workflow (`.github/workflows/docker-publish.yml`) will automatically use these secrets.

---

## Creating a New Release

To publish a new version:

### Using Git Tags

```bash
# Tag the release
git tag -a v3.0.0 -m "Release version 3.0.0"

# Push the tag
git push origin v3.0.0
```

This will automatically:
1. Build multi-architecture Docker images
2. Push to Docker Hub with tags: `3.0.0`, `3.0`, `3`, `latest`
3. Push to GHCR with the same tags

### Using GitHub Releases

1. Go to https://github.com/itsmrshow/home-assistant-mcp-server/releases
2. Click **Draft a new release**
3. Click **Choose a tag** → Create new tag (e.g., `v3.0.0`)
4. Set as target: `main`
5. Fill in release title and description
6. Click **Publish release**

This triggers the same automated build process.

---

## Using Published Images

### Docker Hub

```bash
# Pull latest version
docker pull itsmrshow/home-assistant-mcp-server:latest

# Pull specific version
docker pull itsmrshow/home-assistant-mcp-server:3.0.0

# Use in docker-compose.yml
services:
  ha-mcp-server:
    image: itsmrshow/home-assistant-mcp-server:latest
    # ... rest of config
```

### GitHub Container Registry

```bash
# Pull from GHCR
docker pull ghcr.io/itsmrshow/home-assistant-mcp-server:latest

# Use in docker-compose.yml
services:
  ha-mcp-server:
    image: ghcr.io/itsmrshow/home-assistant-mcp-server:latest
    # ... rest of config
```

---

## Build Status

Check the build status:
- **GitHub Actions:** https://github.com/itsmrshow/home-assistant-mcp-server/actions
- **Docker Hub:** https://hub.docker.com/r/itsmrshow/home-assistant-mcp-server
- **GHCR:** https://github.com/itsmrshow/home-assistant-mcp-server/pkgs/container/home-assistant-mcp-server

---

## Image Tags

| Tag | Description | Updates |
|-----|-------------|---------|
| `latest` | Latest stable release from main branch | On every push to main |
| `3.0.0` | Specific version | Once per release |
| `3.0` | Latest patch of 3.0.x | On every 3.0.x release |
| `3` | Latest minor of 3.x.x | On every 3.x.x release |
| `main` | Latest build from main branch | On every commit to main |

---

## Troubleshooting

### Build Fails with "unauthorized" Error

**Cause:** Docker Hub credentials are incorrect or expired

**Solution:**
1. Verify Docker Hub access token is still valid
2. Check `DOCKER_USERNAME` secret matches your Docker Hub username
3. Regenerate Docker Hub access token and update `DOCKER_PASSWORD` secret

### Build Fails on ARM Platform

**Cause:** QEMU or buildx setup issue

**Solution:**
- The workflow uses `docker/setup-qemu-action@v3` which should handle this
- Check GitHub Actions logs for specific error messages

### Image Not Available on Docker Hub

**Cause:** Push might have failed silently

**Solution:**
1. Check GitHub Actions workflow logs
2. Verify secrets are set correctly
3. Check Docker Hub repository exists and you have write access

---

## Manual Build (Local)

To build multi-architecture images locally:

```bash
# Setup buildx
docker buildx create --use --name multiarch-builder

# Build and push manually
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag itsmrshow/home-assistant-mcp-server:latest \
  --tag itsmrshow/home-assistant-mcp-server:3.0.0 \
  --push \
  .
```

**Note:** You must be logged in to Docker Hub: `docker login`

---

## Security Notes

- Access tokens are more secure than passwords
- Limit token permissions to only what's needed (Read & Write)
- Rotate tokens periodically
- Never commit tokens to git
- Use GitHub Secrets for secure storage

---

## Resources

- **GitHub Actions Documentation:** https://docs.github.com/en/actions
- **Docker Hub:** https://hub.docker.com/
- **Docker Buildx:** https://docs.docker.com/build/buildx/
- **Multi-platform builds:** https://docs.docker.com/build/building/multi-platform/
