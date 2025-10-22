<#
.SYNOPSIS
    Build and push MusicMood Docker images to GitHub Container Registry

.DESCRIPTION
    This script builds both backend and frontend Docker images and pushes them
    to GitHub Container Registry (ghcr.io). Replaces the CD pipeline that fails
    due to GitHub runner disk space limitations.

.PARAMETER Version
    Version tag for the images (e.g., "v1.0.0", "latest")

.PARAMETER Username
    GitHub username (default: VaibhavKarsh)

.PARAMETER SkipBuild
    Skip building images and only push existing local images

.EXAMPLE
    .\scripts\docker-push.ps1 -Version "v1.0.0"
    
.EXAMPLE
    .\scripts\docker-push.ps1 -Version "latest" -Username "myuser"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$false)]
    [string]$Username = "vaibhavkarsh",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"

# Configuration
$REGISTRY = "ghcr.io"
$BACKEND_IMAGE = "$REGISTRY/$Username/musicmood-backend"
$FRONTEND_IMAGE = "$REGISTRY/$Username/musicmood-frontend"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MusicMood Docker Build & Push" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Registry: $REGISTRY" -ForegroundColor White
Write-Host "Version:  $Version" -ForegroundColor White
Write-Host "Backend:  $BACKEND_IMAGE:$Version" -ForegroundColor White
Write-Host "Frontend: $FRONTEND_IMAGE:$Version" -ForegroundColor White
Write-Host ""

# Check if logged in to GitHub Container Registry
Write-Host "Checking GitHub Container Registry login..." -ForegroundColor Yellow
$loginCheck = docker login $REGISTRY 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in to GitHub Container Registry" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please login first:" -ForegroundColor Yellow
    Write-Host "  1. Create a GitHub Personal Access Token (PAT) with 'write:packages' scope"
    Write-Host "  2. Run: echo YOUR_PAT | docker login ghcr.io -u $Username --password-stdin"
    Write-Host ""
    exit 1
}
Write-Host "✅ Logged in to GitHub Container Registry" -ForegroundColor Green
Write-Host ""

if (-not $SkipBuild) {
    # Build Backend Image
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "Building Backend Image..." -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    
    docker build `
        -t "${BACKEND_IMAGE}:${Version}" `
        -t "${BACKEND_IMAGE}:latest" `
        -f Dockerfile.backend `
        .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Backend build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Backend image built successfully" -ForegroundColor Green
    Write-Host ""
    
    # Build Frontend Image
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "Building Frontend Image..." -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    
    docker build `
        -t "${FRONTEND_IMAGE}:${Version}" `
        -t "${FRONTEND_IMAGE}:latest" `
        -f Dockerfile.frontend `
        .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Frontend build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Frontend image built successfully" -ForegroundColor Green
    Write-Host ""
}

# Push Backend Image
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Pushing Backend Image..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

docker push "${BACKEND_IMAGE}:${Version}"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend push failed" -ForegroundColor Red
    exit 1
}

docker push "${BACKEND_IMAGE}:latest"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend latest push failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Backend image pushed successfully" -ForegroundColor Green
Write-Host ""

# Push Frontend Image
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Pushing Frontend Image..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

docker push "${FRONTEND_IMAGE}:${Version}"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend push failed" -ForegroundColor Red
    exit 1
}

docker push "${FRONTEND_IMAGE}:latest"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend latest push failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Frontend image pushed successfully" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "================================================" -ForegroundColor Green
Write-Host "✅ SUCCESS - All images pushed!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Published images:" -ForegroundColor White
Write-Host "  ${BACKEND_IMAGE}:${Version}" -ForegroundColor Cyan
Write-Host "  ${BACKEND_IMAGE}:latest" -ForegroundColor Cyan
Write-Host "  ${FRONTEND_IMAGE}:${Version}" -ForegroundColor Cyan
Write-Host "  ${FRONTEND_IMAGE}:latest" -ForegroundColor Cyan
Write-Host ""
Write-Host "View packages at:" -ForegroundColor White
Write-Host "  https://github.com/$Username?tab=packages" -ForegroundColor Cyan
Write-Host ""
