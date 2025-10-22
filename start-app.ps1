# MusicMood - Unified Startup Script
# Starts both backend and frontend servers together

param(
    [Parameter(Position=0)]
    [ValidateSet('start', 'stop', 'restart', 'status', 'logs', 'help')]
    [string]$Command = 'start'
)

function Show-Help {
    Write-Host "`nMusicMood Unified Startup" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host ".\start-app.ps1 start    - Start backend and frontend" -ForegroundColor White
    Write-Host ".\start-app.ps1 stop     - Stop all services" -ForegroundColor White
    Write-Host ".\start-app.ps1 restart  - Restart all services" -ForegroundColor White
    Write-Host ".\start-app.ps1 status   - Check service status" -ForegroundColor White
    Write-Host ".\start-app.ps1 logs     - View all logs" -ForegroundColor White
    Write-Host "`n"
}

function Start-Services {
    Write-Host "`n" -NoNewline
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " Starting MusicMood Application" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    # Check Docker
    try {
        docker ps | Out-Null
    } catch {
        Write-Host "`n ERROR: Docker is not running!" -ForegroundColor Red
        Write-Host " Please start Docker Desktop first.`n" -ForegroundColor Yellow
        return
    }
    
    Write-Host "`nStarting Docker services..." -ForegroundColor Yellow
    docker-compose up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n ERROR: Failed to start services!`n" -ForegroundColor Red
        return
    }
    
    Write-Host "`nWaiting for services to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Health check
    Write-Host "Checking service health..." -ForegroundColor Yellow
    
    $healthy = $false
    for ($i = 1; $i -le 30; $i++) {
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5 -ErrorAction Stop
            
            if ($health.status -eq "healthy") {
                $healthy = $true
                Write-Host "`n SUCCESS: All services are healthy!`n" -ForegroundColor Green
                
                Write-Host "Service Status:" -ForegroundColor Cyan
                $apiColor = if ($health.services.api.status -eq "healthy") { "Green" } else { "Red" }
                $dbColor = if ($health.services.database.status -eq "healthy") { "Green" } else { "Red" }
                $redisColor = if ($health.services.redis.status -eq "healthy") { "Green" } else { "Red" }
                $ollamaColor = if ($health.services.ollama.status -eq "healthy") { "Green" } else { "Red" }
                
                Write-Host "  Backend:  " -NoNewline
                Write-Host $health.services.api.status -ForegroundColor $apiColor
                Write-Host "  Database: " -NoNewline
                Write-Host $health.services.database.status -ForegroundColor $dbColor
                Write-Host "  Redis:    " -NoNewline
                Write-Host $health.services.redis.status -ForegroundColor $redisColor
                Write-Host "  Ollama:   " -NoNewline
                Write-Host $health.services.ollama.status -ForegroundColor $ollamaColor
                
                if ($health.services.ollama.available_models -gt 0) {
                    Write-Host "  Models:   $($health.services.ollama.available_models) available" -ForegroundColor Green
                }
                
                break
            }
        } catch {
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        }
    }
    
    if (-not $healthy) {
        Write-Host "`n`n WARNING: Health check timeout" -ForegroundColor Yellow
        Write-Host " Services may still be starting. Check logs with:" -ForegroundColor Yellow
        Write-Host " .\start-app.ps1 logs`n" -ForegroundColor Gray
    }
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host " MusicMood is Ready!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nAccess Points:" -ForegroundColor Cyan
    Write-Host "  Frontend:  " -NoNewline; Write-Host "http://localhost:8501" -ForegroundColor White
    Write-Host "  Backend:   " -NoNewline; Write-Host "http://localhost:8001" -ForegroundColor White
    Write-Host "  API Docs:  " -NoNewline; Write-Host "http://localhost:8001/docs" -ForegroundColor White
    
    Write-Host "`nQuick Commands:" -ForegroundColor Cyan
    Write-Host "  .\start-app.ps1 stop     - Stop all services" -ForegroundColor Gray
    Write-Host "  .\start-app.ps1 restart  - Restart services" -ForegroundColor Gray
    Write-Host "  .\start-app.ps1 status   - Check status" -ForegroundColor Gray
    Write-Host "  .\start-app.ps1 logs     - View logs`n" -ForegroundColor Gray
}

function Stop-Services {
    Write-Host "`nStopping all services..." -ForegroundColor Yellow
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " SUCCESS: All services stopped!`n" -ForegroundColor Green
    } else {
        Write-Host " ERROR: Failed to stop services!`n" -ForegroundColor Red
    }
}

function Restart-Services {
    Stop-Services
    Start-Sleep -Seconds 2
    Start-Services
}

function Show-ServiceStatus {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host " MusicMood Service Status" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    Write-Host "`nDocker Containers:" -ForegroundColor Yellow
    docker-compose ps
    
    Write-Host "`nHealth Check:" -ForegroundColor Yellow
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5
        
        $statusColor = if ($health.status -eq "healthy") { "Green" } else { "Yellow" }
        Write-Host "  Overall:    " -NoNewline
        Write-Host $health.status -ForegroundColor $statusColor
        Write-Host "  Environment: $($health.environment)" -ForegroundColor White
        
        Write-Host "`n  Services:" -ForegroundColor Cyan
        $apiColor = if ($health.services.api.status -eq "healthy") { "Green" } else { "Red" }
        $dbColor = if ($health.services.database.status -eq "healthy") { "Green" } else { "Red" }
        $redisColor = if ($health.services.redis.status -eq "healthy") { "Green" } else { "Red" }
        $ollamaColor = if ($health.services.ollama.status -eq "healthy") { "Green" } else { "Red" }
        
        Write-Host "    API:      " -NoNewline
        Write-Host $health.services.api.status -ForegroundColor $apiColor
        Write-Host "    Database: " -NoNewline
        Write-Host $health.services.database.status -NoNewline -ForegroundColor $dbColor
        Write-Host " ($($health.services.database.tables) tables)" -ForegroundColor Gray
        Write-Host "    Redis:    " -NoNewline
        Write-Host $health.services.redis.status -NoNewline -ForegroundColor $redisColor
        Write-Host " ($($health.services.redis.used_memory_human))" -ForegroundColor Gray
        Write-Host "    Ollama:   " -NoNewline
        Write-Host $health.services.ollama.status -ForegroundColor $ollamaColor
        
        if ($health.services.ollama.status -eq "healthy") {
            Write-Host "      Models: $($health.services.ollama.available_models) available" -ForegroundColor Green
            Write-Host "      Active: $($health.services.ollama.configured_model)" -ForegroundColor White
        }
        
    } catch {
        Write-Host "   Backend not responding" -ForegroundColor Red
    }
    
    Write-Host "`nFrontend:" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "   Running (HTTP 200)" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Not responding" -ForegroundColor Red
    }
    
    Write-Host ""
}

function Show-AllLogs {
    Write-Host "`nShowing logs (Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f --tail=50
}

# Execute command
switch ($Command) {
    'start'   { Start-Services }
    'stop'    { Stop-Services }
    'restart' { Restart-Services }
    'status'  { Show-ServiceStatus }
    'logs'    { Show-AllLogs }
    'help'    { Show-Help }
    default   { Show-Help }
}
