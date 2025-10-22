# Docker Registry Setup Guide

## Overview

Due to GitHub Actions free runner disk space limitations (~14GB available, 40GB+ needed for builds), **Docker images must be built and pushed locally** instead of via CI/CD pipelines.

## Why Local Builds?

GitHub's free runners consistently fail with **"No space left on device"** errors when building Python Docker images with Poetry dependencies. Even after aggressive cleanup (removing 50GB+ of unused packages), the builds still exceed available disk space.

**Solution**: Build images on your local machine (which has sufficient disk space) and push to GitHub Container Registry.

## Prerequisites

1. **Docker Desktop installed and running**
2. **GitHub Personal Access Token (PAT)** with `write:packages` scope

## Setup Steps

### 1. Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name it: `MusicMood Docker Push`
4. Select scope: **`write:packages`**
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

### 2. Login to GitHub Container Registry

```powershell
# Replace YOUR_TOKEN with your actual token
echo YOUR_TOKEN | docker login ghcr.io -u vaibhavkarsh --password-stdin
```

Expected output:
```
Login Succeeded
```

### 3. Build and Push Images

Use the provided script:

```powershell
# Build and push with version tag
.\scripts\docker-push.ps1 -Version "v1.0.0"

# Build and push as latest
.\scripts\docker-push.ps1 -Version "latest"
```

The script will:
1. ✅ Check registry login
2. 🔨 Build backend image (`Dockerfile.backend`)
3. 🔨 Build frontend image (`Dockerfile.frontend`)
4. ⬆️ Push backend to `ghcr.io/vaibhavkarsh/musicmood-backend`
5. ⬆️ Push frontend to `ghcr.io/vaibhavkarsh/musicmood-frontend`
6. 📦 Tag both as `latest` and your specified version

### 4. Verify Published Images

View your packages at:
https://github.com/VaibhavKarsh?tab=packages

## Script Options

### Basic Usage
```powershell
.\scripts\docker-push.ps1 -Version "v1.0.1"
```

### Custom Username
```powershell
.\scripts\docker-push.ps1 -Version "v1.0.0" -Username "myusername"
```

### Skip Build (Push Only)
```powershell
# If images are already built locally
.\scripts\docker-push.ps1 -Version "v1.0.0" -SkipBuild
```

## Manual Build & Push

If you prefer manual commands:

```powershell
# Backend
docker build -t ghcr.io/vaibhavkarsh/musicmood-backend:v1.0.0 -f Dockerfile.backend .
docker build -t ghcr.io/vaibhavkarsh/musicmood-backend:latest -f Dockerfile.backend .
docker push ghcr.io/vaibhavkarsh/musicmood-backend:v1.0.0
docker push ghcr.io/vaibhavkarsh/musicmood-backend:latest

# Frontend
docker build -t ghcr.io/vaibhavkarsh/musicmood-frontend:v1.0.0 -f Dockerfile.frontend .
docker build -t ghcr.io/vaibhavkarsh/musicmood-frontend:latest -f Dockerfile.frontend .
docker push ghcr.io/vaibhavkarsh/musicmood-frontend:v1.0.0
docker push ghcr.io/vaibhavkarsh/musicmood-frontend:latest
```

## Troubleshooting

### Error: "denied: permission_denied"
- **Cause**: Not logged in or token lacks `write:packages` scope
- **Fix**: Re-login with correct token and scope

### Error: "repository does not exist"
- **Cause**: First time pushing to this repository
- **Fix**: The push will create the repository automatically

### Build fails locally
- **Cause**: Insufficient disk space or Docker issues
- **Fix**: 
  ```powershell
  docker system prune -af --volumes  # Free up space
  docker-compose down -v             # Stop local containers
  ```

## CI/CD Status

### ✅ Enabled
- **Code Quality Checks**: Black, isort, flake8, mypy (lightweight, ~2GB)

### ❌ Disabled (Disk Space Issues)
- **Unit Tests**: Requires PostgreSQL + Redis services
- **Docker Build Test**: Requires 40GB+ disk space
- **Docker Push**: Requires 40GB+ disk space

All disabled jobs are commented out in workflow files and can be re-enabled if using:
- GitHub Teams/Enterprise (larger runners)
- Self-hosted runners
- External CI/CD platforms (CircleCI, GitLab CI with larger runners)

## Best Practices

1. **Version Tags**: Use semantic versioning (v1.0.0, v1.1.0, etc.)
2. **Always tag `latest`**: Makes pulling easier for users
3. **Test locally first**: Run `.\start-app.ps1 start` to verify images work
4. **Clean builds**: Occasionally run `docker system prune -af` to free space

## Security Notes

- ✅ PAT token stored locally (not in Git)
- ✅ Docker credentials stored in Docker Desktop keychain
- ✅ Images are public by default on ghcr.io
- ⚠️ Never commit your PAT token to Git

## Alternative Solutions

If local builds are not feasible:

1. **Use Docker Hub**: Free tier, no disk space issues
2. **GitLab CI**: Offers larger runners on free tier
3. **Self-hosted runner**: Set up your own machine as GitHub Actions runner
4. **GitHub Packages**: Upgrade to Teams/Enterprise for larger runners

## Summary

GitHub's free runners simply don't have enough disk space for complex Python+Poetry Docker builds. Local builds are the most practical solution for free-tier users. The provided script makes this process simple and reproducible.

**Questions?** Open an issue on GitHub!
