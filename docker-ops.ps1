# MusicMood Docker Management Script for Windows
# Usage: .\docker-ops.ps1 <command>

param(
    [Parameter(Position=0)]
    [ValidateSet('build', 'up', 'down', 'restart', 'logs', 'logs-backend', 'logs-frontend', 
                 'clean', 'rebuild', 'shell-backend', 'shell-frontend', 'shell-db', 
                 'migrate', 'ps', 'health', 'backup-db', 'pull-models', 'list-models', 
                 'shell-ollama', 'logs-ollama', 'help')]
    [string]$Command = 'help'
)

function Show-Help {
    Write-Host "`nMusicMood Docker Commands" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host ".\docker-ops.ps1 build         - Build all Docker images"
    Write-Host ".\docker-ops.ps1 up            - Start all services"
    Write-Host ".\docker-ops.ps1 down          - Stop all services"
    Write-Host ".\docker-ops.ps1 restart       - Restart all services"
    Write-Host ".\docker-ops.ps1 logs          - View logs (all services)"
    Write-Host ".\docker-ops.ps1 logs-backend  - View backend logs"
    Write-Host ".\docker-ops.ps1 logs-frontend - View frontend logs"
    Write-Host ".\docker-ops.ps1 logs-ollama   - View Ollama logs"
    Write-Host ".\docker-ops.ps1 clean         - Stop and remove all containers, volumes"
    Write-Host ".\docker-ops.ps1 rebuild       - Clean build and start"
    Write-Host ".\docker-ops.ps1 shell-backend - Access backend container shell"
    Write-Host ".\docker-ops.ps1 shell-frontend- Access frontend container shell"
    Write-Host ".\docker-ops.ps1 shell-db      - Access PostgreSQL shell"
    Write-Host ".\docker-ops.ps1 shell-ollama  - Access Ollama container shell"
    Write-Host ".\docker-ops.ps1 migrate       - Run database migrations"
    Write-Host ".\docker-ops.ps1 ps            - Show running containers"
    Write-Host ".\docker-ops.ps1 health        - Check service health"
    Write-Host ".\docker-ops.ps1 backup-db     - Backup database"
    Write-Host ".\docker-ops.ps1 pull-models   - Pull Ollama models"
    Write-Host ".\docker-ops.ps1 list-models   - List available Ollama models"
    Write-Host "`n"
}

function Build-Images {
    Write-Host "🔨 Building Docker images..." -ForegroundColor Yellow
    docker-compose build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build complete!" -ForegroundColor Green
    }
}

function Start-Services {
    Write-Host "🚀 Starting all services..." -ForegroundColor Yellow
    docker-compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Services started!" -ForegroundColor Green
        Write-Host "Frontend: http://localhost:8501" -ForegroundColor Cyan
        Write-Host "Backend API: http://localhost:8001" -ForegroundColor Cyan
        Write-Host "API Docs: http://localhost:8001/docs" -ForegroundColor Cyan
    }
}

function Stop-Services {
    Write-Host "🛑 Stopping all services..." -ForegroundColor Yellow
    docker-compose down
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Services stopped!" -ForegroundColor Green
    }
}

function Restart-Services {
    Write-Host "🔄 Restarting all services..." -ForegroundColor Yellow
    docker-compose restart
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Services restarted!" -ForegroundColor Green
    }
}

function Show-Logs {
    Write-Host "📋 Showing logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f
}

function Show-BackendLogs {
    Write-Host "📋 Showing backend logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f backend
}

function Show-FrontendLogs {
    Write-Host "📋 Showing frontend logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f frontend
}

function Show-OllamaLogs {
    Write-Host "📋 Showing Ollama logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f ollama
}

function Pull-OllamaModels {
    Write-Host "🤖 Pulling Ollama models..." -ForegroundColor Yellow
    Write-Host "This may take several minutes depending on your internet connection." -ForegroundColor Yellow
    
    Write-Host "`n📥 Pulling gemma3:4b (~3.3GB)..." -ForegroundColor Cyan
    docker-compose exec ollama ollama pull gemma3:4b
    
    Write-Host "`n📥 Pulling qwen3:4b (~2.5GB)..." -ForegroundColor Cyan
    docker-compose exec ollama ollama pull qwen3:4b
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ All models pulled successfully!" -ForegroundColor Green
        Write-Host "`n📋 Available models:" -ForegroundColor Cyan
        docker-compose exec ollama ollama list
    }
}

function List-OllamaModels {
    Write-Host "📋 Available Ollama models:" -ForegroundColor Yellow
    docker-compose exec ollama ollama list
}

function Shell-Ollama {
    Write-Host "🐚 Accessing Ollama container shell..." -ForegroundColor Yellow
    docker-compose exec ollama bash
}

function Clean-All {
    Write-Host "⚠️  WARNING: This will remove all containers and volumes!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (yes/no)"
    if ($confirm -eq "yes") {
        docker-compose down -v
        Write-Host "✅ All data removed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Operation cancelled" -ForegroundColor Yellow
    }
}

function Rebuild-All {
    Write-Host "🔄 Rebuilding from scratch..." -ForegroundColor Yellow
    Clean-All
    Build-Images
    Start-Services
}

function Shell-Backend {
    Write-Host "🐚 Accessing backend container shell..." -ForegroundColor Yellow
    docker-compose exec backend bash
}

function Shell-Frontend {
    Write-Host "🐚 Accessing frontend container shell..." -ForegroundColor Yellow
    docker-compose exec frontend bash
}

function Shell-Database {
    Write-Host "🐚 Accessing PostgreSQL shell..." -ForegroundColor Yellow
    docker-compose exec postgres psql -U musicmood_user -d musicmood
}

function Run-Migrations {
    Write-Host "🔄 Running database migrations..." -ForegroundColor Yellow
    docker-compose exec backend alembic upgrade head
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Migrations complete!" -ForegroundColor Green
    }
}

function Show-Status {
    Write-Host "📊 Container status:" -ForegroundColor Yellow
    docker-compose ps
}

function Check-Health {
    Write-Host "`n🔍 Checking service health..." -ForegroundColor Yellow
    docker-compose ps
    
    Write-Host "`n🔍 Backend Health:" -ForegroundColor Cyan
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5
        Write-Host "✅ Backend: OK" -ForegroundColor Green
        $response | ConvertTo-Json
    } catch {
        Write-Host "❌ Backend: Not responding" -ForegroundColor Red
    }
    
    Write-Host "`n🔍 Frontend Health:" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Frontend: OK" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Frontend: Not responding" -ForegroundColor Red
    }
    
    Write-Host "`n🔍 Database Health:" -ForegroundColor Cyan
    docker-compose exec postgres pg_isready -U musicmood_user
    
    Write-Host "`n🔍 Redis Health:" -ForegroundColor Cyan
    docker-compose exec redis redis-cli ping
    
    Write-Host "`n🔍 Ollama Health:" -ForegroundColor Cyan
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5
        if ($response.models) {
            Write-Host "✅ Ollama: OK - $($response.models.Count) model(s) available" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Ollama: Running but no models installed" -ForegroundColor Yellow
            Write-Host "   Run '.\docker-ops.ps1 pull-models' to download models" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Ollama: Not responding" -ForegroundColor Red
    }
}

function Backup-Database {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "backup_$timestamp.sql"
    Write-Host "💾 Backing up database to $filename..." -ForegroundColor Yellow
    docker-compose exec postgres pg_dump -U musicmood_user musicmood | Out-File -FilePath $filename -Encoding UTF8
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database backed up to $filename" -ForegroundColor Green
    }
}

# Execute command
switch ($Command) {
    'build'         { Build-Images }
    'up'            { Start-Services }
    'down'          { Stop-Services }
    'restart'       { Restart-Services }
    'logs'          { Show-Logs }
    'logs-backend'  { Show-BackendLogs }
    'logs-frontend' { Show-FrontendLogs }
    'logs-ollama'   { Show-OllamaLogs }
    'clean'         { Clean-All }
    'rebuild'       { Rebuild-All }
    'shell-backend' { Shell-Backend }
    'shell-frontend'{ Shell-Frontend }
    'shell-db'      { Shell-Database }
    'shell-ollama'  { Shell-Ollama }
    'migrate'       { Run-Migrations }
    'ps'            { Show-Status }
    'health'        { Check-Health }
    'backup-db'     { Backup-Database }
    'pull-models'   { Pull-OllamaModels }
    'list-models'   { List-OllamaModels }
    'help'          { Show-Help }
    default         { Show-Help }
}
