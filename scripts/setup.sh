#!/bin/bash

# MetaMystic Setup Script
# Sets up the development environment for MetaMystic

set -e  # Exit on any error

echo "🔮 Setting up MetaMystic Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Create environment file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating environment configuration..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env from template"
    echo "⚠️  Please edit backend/.env with your API keys and configuration"
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/decks
mkdir -p data/spreads
mkdir -p partners/metamystic
mkdir -p uploads

# Set up backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Create requirements.txt from pyproject.toml
echo "📋 Generating requirements.txt..."
if command -v poetry &> /dev/null; then
    poetry export -f requirements.txt --output requirements.txt --without-hashes
else
    echo "⚠️  Poetry not found. Creating basic requirements.txt..."
    cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
pydantic[email]==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiofiles==23.2.1
httpx==0.25.2
pillow==10.1.0
kerykeion==4.10.3
openai==1.3.7
anthropic==0.7.7
google-generativeai==0.3.2
boto3==1.34.0
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1
EOF
fi

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Go back to root directory
cd ..

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker services are running"
else
    echo "❌ Failed to start Docker services"
    exit 1
fi

# Initialize database
echo "🗄️  Initializing database..."
cd backend
python -c "
import asyncio
from src.core.database import engine, Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Database tables created')

asyncio.run(init_db())
"

# Create initial migration
if [ ! -d "alembic/versions" ]; then
    echo "📝 Creating initial database migration..."
    mkdir -p alembic/versions
    alembic revision --autogenerate -m "Initial migration"
fi

cd ..

echo ""
echo "🎉 MetaMystic setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "  1. Edit backend/.env with your API keys"
echo "  2. Run 'docker-compose up -d' to start all services"
echo "  3. Run 'cd backend && python -m uvicorn src.app:app --reload' to start the API"
echo "  4. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "🔧 Useful commands:"
echo "  - Run tests: ./scripts/test_all.sh"
echo "  - Start services: docker-compose up -d"
echo "  - Stop services: docker-compose down"
echo "  - View logs: docker-compose logs -f"
echo ""
echo "✨ Happy coding with MetaMystic!"
