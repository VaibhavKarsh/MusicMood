# MusicMood Docker Deployment Guide

## 🚀 Quick Start with Docker

### Prerequisites
- Docker Desktop installed and running
- Docker Compose v2.0+
- Ollama running on your host machine (for AI features)
- Spotify Developer credentials

### 1. Environment Setup

Copy the Docker environment template:
```bash
cp .env.docker .env
```

Edit `.env` and add your credentials:
- `SPOTIFY_CLIENT_ID` - From Spotify Developer Dashboard
- `SPOTIFY_CLIENT_SECRET` - From Spotify Developer Dashboard
- `OLLAMA_BASE_URL` - Leave as `http://host.docker.internal:11434` if Ollama is on host

### 2. Start All Services

```bash
# Start core services (backend, frontend, database, redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Access the Application

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6379

### 4. Optional: Start Management Tools

```bash
# Start with pgAdmin and Redis Commander
docker-compose --profile tools up -d

# Access tools:
# - pgAdmin: http://localhost:5050 (admin@musicmood.local / admin)
# - Redis Commander: http://localhost:8081
```

## 🔧 Development Workflow

### Hot Reload
The containers are configured with volume mounts for hot reload during development:
- Backend: `./app` is mounted, code changes trigger auto-reload
- Frontend: `./app/frontend` is mounted, Streamlit auto-reloads

### Database Migrations

Run migrations inside the container:
```bash
docker-compose exec backend alembic upgrade head
```

Create new migration:
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

## 🛠️ Common Operations

### Rebuild Containers
```bash
# Rebuild after code changes
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild with no cache
docker-compose build --no-cache
```

### Stop Services
```bash
# Stop all
docker-compose down

# Stop and remove volumes (WARNING: deletes data!)
docker-compose down -v
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Access Container Shell
```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend bash

# Database shell
docker-compose exec postgres psql -U musicmood_user -d musicmood
```

## 🐛 Troubleshooting

### Backend won't start
1. Check Ollama is running: `curl http://localhost:11434/api/tags`
2. Check logs: `docker-compose logs backend`
3. Verify environment variables: `docker-compose exec backend env`

### Frontend can't reach backend
1. Ensure backend is healthy: `docker-compose ps`
2. Check network: `docker network inspect musicmood_musicmood-network`
3. Test API: `curl http://localhost:8001/health`

### Database connection issues
1. Check postgres health: `docker-compose ps postgres`
2. Test connection: `docker-compose exec postgres pg_isready`
3. View logs: `docker-compose logs postgres`

### Port conflicts
If ports are already in use, edit `docker-compose.yml`:
- Backend: Change `8001:8001` to `8002:8001`
- Frontend: Change `8501:8501` to `8502:8501`
- PostgreSQL: Change `5433:5432` to `5434:5432`

## 📊 Health Checks

All services have health checks configured:

```bash
# Check all services health
docker-compose ps

# Backend health endpoint
curl http://localhost:8001/health

# Frontend health endpoint
curl http://localhost:8501/_stcore/health

# Database health
docker-compose exec postgres pg_isready -U musicmood_user

# Redis health
docker-compose exec redis redis-cli ping
```

## 🔒 Security Notes

- Default passwords are in `.env.docker` - **CHANGE THEM** for production
- The `.env` file is gitignored - never commit credentials
- Backend runs as non-root user (appuser)
- Frontend runs as non-root user (appuser)

## 📦 Production Deployment

For production deployment:
1. Use production-grade PostgreSQL (not containerized)
2. Use managed Redis service
3. Set strong passwords in environment variables
4. Enable SSL/TLS for all connections
5. Use Docker secrets instead of environment variables
6. Configure proper resource limits
7. Set up monitoring and logging

## 🔄 Backup and Restore

### Backup Database
```bash
docker-compose exec postgres pg_dump -U musicmood_user musicmood > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker-compose exec -T postgres psql -U musicmood_user -d musicmood
```

### Backup Redis
```bash
docker-compose exec redis redis-cli SAVE
docker cp musicmood-redis:/data/dump.rdb ./redis-backup.rdb
```

## 📈 Resource Limits

Default resource limits in `docker-compose.yml`:
- PostgreSQL: No limits (adjust based on data size)
- Redis: 512MB memory limit (set in redis.conf)
- Backend: No limits (adjust based on traffic)
- Frontend: No limits (adjust based on concurrent users)

Add resource limits if needed:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```
