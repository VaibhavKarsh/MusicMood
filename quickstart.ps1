# MusicMood Quick Start Script for Windows
# This script helps you set up the development environment quickly

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  MusicMood Quick Start - Phase 1 Setup" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Function to check if service is running on a port
function Test-Port {
    param($Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
        return $connection
    }
    catch {
        return $false
    }
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "[OK] $pythonVersion found" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Poetry
if (Test-Command poetry) {
    $poetryVersion = poetry --version
    Write-Host "[OK] $poetryVersion found" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] Poetry not found. Install from: https://python-poetry.org/" -ForegroundColor Red
    exit 1
}

# Check Docker
if (Test-Command docker) {
    Write-Host "[OK] Docker found" -ForegroundColor Green
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Docker is running" -ForegroundColor Green
    }
    else {
        Write-Host "[WARNING] Docker is not running. Start Docker Desktop" -ForegroundColor Yellow
    }
}
else {
    Write-Host "[WARNING] Docker not found. Install Docker Desktop for easier setup" -ForegroundColor Yellow
}

# Check Ollama
if (Test-Command ollama) {
    Write-Host "[OK] Ollama found" -ForegroundColor Green
    
    # Check if Ollama service is running
    if (Test-Port 11434) {
        Write-Host "[OK] Ollama service is running on port 11434" -ForegroundColor Green
    }
    else {
        Write-Host "[WARNING] Ollama service not running. Starting..." -ForegroundColor Yellow
        Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
    }
    
    # Check Mistral model
    $models = ollama list 2>&1 | Out-String
    if ($models -match "mistral") {
        Write-Host "[OK] Mistral model is installed" -ForegroundColor Green
    }
    else {
        Write-Host "[INFO] Pulling Mistral model (this will take 5-10 minutes)..." -ForegroundColor Yellow
        ollama pull mistral
    }
}
else {
    Write-Host "[TODO] Ollama not found. Download from: https://ollama.ai/download" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Starting Services with Docker Compose" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Command docker) {
    Write-Host "Starting PostgreSQL and Redis..." -ForegroundColor Yellow
    docker-compose up -d postgres redis
    
    Write-Host ""
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Check services
    if (Test-Port 5432) {
        Write-Host "[OK] PostgreSQL is running on port 5432" -ForegroundColor Green
    }
    else {
        Write-Host "[ERROR] PostgreSQL failed to start" -ForegroundColor Red
    }
    
    if (Test-Port 6379) {
        Write-Host "[OK] Redis is running on port 6379" -ForegroundColor Green
    }
    else {
        Write-Host "[ERROR] Redis failed to start" -ForegroundColor Red
    }
}
else {
    Write-Host "[SKIP] Docker not available - manual setup required" -ForegroundColor Yellow
    Write-Host "See SETUP_GUIDE.md for manual PostgreSQL and Redis installation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Environment Configuration" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check .env file
if (Test-Path ".env") {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
    
    # Check for API keys
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "SPOTIFY_CLIENT_ID=\w+") {
        Write-Host "[OK] Spotify credentials configured" -ForegroundColor Green
    }
    else {
        Write-Host "[TODO] Add Spotify credentials to .env" -ForegroundColor Yellow
        Write-Host "       Get from: https://developer.spotify.com/dashboard" -ForegroundColor Gray
    }
    
    if ($envContent -match "OPENWEATHER_API_KEY=\w+") {
        Write-Host "[OK] OpenWeather API key configured" -ForegroundColor Green
    }
    else {
        Write-Host "[TODO] Add OpenWeather API key to .env" -ForegroundColor Yellow
        Write-Host "       Get from: https://openweathermap.org/api" -ForegroundColor Gray
    }
}
else {
    Write-Host "[ERROR] .env file not found" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env created. Please edit it with your API credentials" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Running Phase 1 Verification" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
poetry install --no-interaction

Write-Host ""
Write-Host "Running verification script..." -ForegroundColor Yellow
poetry run python verify_phase1.py

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. If any checks failed, follow the instructions in SETUP_GUIDE.md" -ForegroundColor White
Write-Host "2. Add your Spotify and OpenWeather API credentials to .env" -ForegroundColor White
Write-Host "3. Run: poetry run python verify_phase1.py" -ForegroundColor White
Write-Host "4. When all checks pass, you're ready for Phase 2!" -ForegroundColor White
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  poetry shell                    - Activate virtual environment" -ForegroundColor Gray
Write-Host "  docker-compose logs -f          - View service logs" -ForegroundColor Gray
Write-Host "  docker-compose down             - Stop services" -ForegroundColor Gray
Write-Host "  poetry run python verify_phase1.py - Run verification" -ForegroundColor Gray
Write-Host ""
