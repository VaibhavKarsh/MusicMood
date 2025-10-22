.PHONY: help build up down restart logs clean rebuild

# Default target
help:
	@echo "MusicMood Docker Commands"
	@echo "========================="
	@echo "make build         - Build all Docker images"
	@echo "make up            - Start all services"
	@echo "make down          - Stop all services"
	@echo "make restart       - Restart all services"
	@echo "make logs          - View logs (all services)"
	@echo "make logs-backend  - View backend logs"
	@echo "make logs-frontend - View frontend logs"
	@echo "make clean         - Stop and remove all containers, volumes"
	@echo "make rebuild       - Clean build and start"
	@echo "make shell-backend - Access backend container shell"
	@echo "make shell-db      - Access PostgreSQL shell"
	@echo "make migrate       - Run database migrations"
	@echo "make ps            - Show running containers"
	@echo "make health        - Check service health"

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:8501"
	@echo "Backend API: http://localhost:8001"
	@echo "API Docs: http://localhost:8001/docs"

# Start with tools (pgAdmin, Redis Commander)
up-tools:
	docker-compose --profile tools up -d

# Stop all services
down:
	docker-compose down

# Restart all services
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# Backend logs
logs-backend:
	docker-compose logs -f backend

# Frontend logs
logs-frontend:
	docker-compose logs -f frontend

# Clean everything (including volumes)
clean:
	docker-compose down -v
	@echo "⚠️  All data has been removed!"

# Rebuild from scratch
rebuild: clean build up

# Access backend shell
shell-backend:
	docker-compose exec backend bash

# Access frontend shell
shell-frontend:
	docker-compose exec frontend bash

# Access database shell
shell-db:
	docker-compose exec postgres psql -U musicmood_user -d musicmood

# Run migrations
migrate:
	docker-compose exec backend alembic upgrade head

# Create new migration
migration:
	@read -p "Enter migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"

# Show running containers
ps:
	docker-compose ps

# Health check
health:
	@echo "Checking service health..."
	@docker-compose ps
	@echo "\n🔍 Backend Health:"
	@curl -s http://localhost:8001/health | python -m json.tool || echo "❌ Backend not responding"
	@echo "\n🔍 Frontend Health:"
	@curl -s http://localhost:8501/_stcore/health | python -m json.tool || echo "❌ Frontend not responding"
	@echo "\n🔍 Database Health:"
	@docker-compose exec postgres pg_isready -U musicmood_user || echo "❌ Database not ready"
	@echo "\n🔍 Redis Health:"
	@docker-compose exec redis redis-cli ping || echo "❌ Redis not responding"

# Backup database
backup-db:
	docker-compose exec postgres pg_dump -U musicmood_user musicmood > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backed up!"

# Restore database
restore-db:
	@read -p "Enter backup file path: " file; \
	cat $$file | docker-compose exec -T postgres psql -U musicmood_user -d musicmood
	@echo "✅ Database restored!"
