# MetaMystic Development Makefile

.PHONY: help setup up down logs test clean install format lint type-check dev

# Default target
help:
	@echo "🔮 MetaMystic Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup     - Initial project setup"
	@echo "  make install   - Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev       - Start development server"
	@echo "  make up        - Start all services with Docker"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View service logs"
	@echo ""
	@echo "Code Quality:"
	@echo "  make test      - Run all tests"
	@echo "  make format    - Format code with black and isort"
	@echo "  make lint      - Run linting with flake8"
	@echo "  make type-check - Run type checking with mypy"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make reset     - Reset database and restart services"

# Initial project setup
setup:
	@echo "🔮 Setting up MetaMystic..."
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

# Install dependencies
install:
	@echo "📥 Installing dependencies..."
	@cd backend && pip install -r requirements.txt

# Start development server
dev:
	@echo "🚀 Starting development server..."
	@cd backend && python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# Start all services
up:
	@echo "🐳 Starting all services..."
	@docker-compose up -d

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	@docker-compose down

# View logs
logs:
	@echo "📋 Viewing service logs..."
	@docker-compose logs -f

# Run all tests
test:
	@echo "🧪 Running tests..."
	@chmod +x scripts/test_all.sh
	@./scripts/test_all.sh

# Format code
format:
	@echo "🎨 Formatting code..."
	@cd backend && black src/ tests/ || echo "Black not installed"
	@cd backend && isort src/ tests/ || echo "isort not installed"

# Run linting
lint:
	@echo "🔍 Running linting..."
	@cd backend && flake8 src/ tests/ || echo "flake8 not installed"

# Run type checking
type-check:
	@echo "🔬 Running type checking..."
	@cd backend && mypy src/ || echo "mypy not installed"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Reset database and restart
reset:
	@echo "🔄 Resetting database and restarting services..."
	@docker-compose down -v
	@docker-compose up -d postgres redis
	@sleep 5
	@cd backend && alembic upgrade head

# Database migrations
migrate:
	@echo "📝 Creating database migration..."
	@cd backend && alembic revision --autogenerate -m "$(msg)"

# Apply migrations
upgrade:
	@echo "⬆️  Applying database migrations..."
	@cd backend && alembic upgrade head

# Downgrade migrations
downgrade:
	@echo "⬇️  Downgrading database migrations..."
	@cd backend && alembic downgrade -1

# Build Docker images
build:
	@echo "🏗️  Building Docker images..."
	@docker-compose build

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	@docker-compose -f docker-compose.prod.yml up -d

# Check system health
health:
	@echo "🏥 Checking system health..."
	@curl -f http://localhost:8000/health || echo "API not responding"
	@docker-compose ps

# Generate API documentation
docs:
	@echo "📚 Generating API documentation..."
	@echo "Visit http://localhost:8000/docs for interactive API docs"
	@echo "Visit http://localhost:8000/redoc for alternative docs"

# Backup database
backup:
	@echo "💾 Creating database backup..."
	@docker-compose exec postgres pg_dump -U metamystic metamystic > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database
restore:
	@echo "🔄 Restoring database from backup..."
	@docker-compose exec -T postgres psql -U metamystic metamystic < $(file)

# Show project status
status:
	@echo "📊 MetaMystic Project Status"
	@echo ""
	@echo "Docker Services:"
	@docker-compose ps
	@echo ""
	@echo "API Health:"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "API not responding"
	@echo ""
	@echo "Database Status:"
	@docker-compose exec postgres pg_isready -U metamystic || echo "Database not ready"
