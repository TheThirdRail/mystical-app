# MetaMystic - Spiritual Reading Platform

A Python-first spiritual reading platform providing astrology (tropical & sidereal), Chinese zodiac, numerology, and tarot readings with AI-powered interpretations.

## 🔮 Features

- **Multi-discipline readings**: Astrology, Chinese zodiac, numerology, and tarot
- **Partner system**: Custom personas with unique decks, spreads, and AI voice
- **Multi-provider LLM**: Support for OpenAI, Anthropic, Google, and Meta
- **Revenue tracking**: Automatic partner earnings calculation
- **Mobile & Web**: React Native mobile app and React web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for mobile client)

### Automated Setup

```bash
# Run the setup script
make setup

# Or manually:
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

1. **Environment configuration**:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys and database settings
```

2. **Start services**:
```bash
make up
# Or: docker-compose up -d
```

3. **Start development server**:
```bash
make dev
# Or: cd backend && python -m uvicorn src.app:app --reload
```

4. **Run tests**:
```bash
make test
# Or: ./scripts/test_all.sh
```

### API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Architecture

```
backend/
├── src/
│   ├── core/           # Pure calculation modules
│   │   ├── astro.py    # Astrology calculations
│   │   ├── numerology.py
│   │   ├── tarot.py
│   │   └── zodiac.py
│   ├── services/       # Business logic
│   │   ├── ai/         # LLM providers
│   │   ├── auth/       # Authentication
│   │   └── readings/   # Reading orchestration
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   └── api/           # FastAPI routes
├── data/              # Static data (decks, spreads)
├── partners/          # Partner-specific assets
└── tests/            # Test suite
```

## Partner Integration

Partners can customize their readings by:

1. **Persona setup**: Photo, bio, and AI voice customization
2. **Custom decks**: Upload tarot deck images and metadata
3. **Custom spreads**: Define unique card layouts
4. **Rule overrides**: Modify interpretation logic

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/metamystic

# LLM Providers (choose one or more)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Storage
S3_BUCKET=metamystic-assets
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key

# Security
JWT_SECRET=your_jwt_secret
```

## 🛠️ Development Commands

```bash
# Setup and installation
make setup          # Initial project setup
make install        # Install dependencies

# Development
make dev           # Start development server
make up            # Start all services
make down          # Stop all services
make logs          # View service logs

# Code quality
make test          # Run all tests
make format        # Format code
make lint          # Run linting
make type-check    # Run type checking

# Database
make migrate       # Create migration
make upgrade       # Apply migrations
make reset         # Reset database

# Utilities
make clean         # Clean temporary files
make health        # Check system health
make status        # Show project status
```

## 📊 Current Implementation Status

### ✅ Completed
- **Core Architecture**: FastAPI app with async database, Redis caching
- **Database Models**: All entities (User, Partner, Persona, Deck, Card, Spread, Reading, Payment)
- **Calculation Engines**:
  - Astrology (Kerykeion integration, tropical/sidereal)
  - Numerology (core numbers, life path, expression, etc.)
  - Chinese Zodiac (animals, elements, compatibility)
  - Tarot (card drawing, spreads, interpretations)
- **LLM Integration**: Multi-provider support (OpenAI, Anthropic, Google, Meta)
- **API Endpoints**: Complete REST API with validation
- **Reading Service**: Orchestrates all calculations and AI interpretation
- **Data Files**: Default tarot deck (RWS) and spreads
- **Development Tools**: Docker setup, testing framework, scripts

### 🚧 In Progress / TODO
- **Authentication**: JWT implementation (stubs created)
- **Partner Management**: Full CRUD operations
- **File Upload**: Image handling for decks/personas
- **Database Migrations**: Alembic setup (needs initial migration)
- **Minor Arcana**: Complete tarot deck with all 78 cards
- **Mobile Client**: React Native app
- **Web Client**: React frontend
- **Payment Integration**: Stripe/PayPal integration
- **Admin Dashboard**: Partner management interface

### 🎯 Next Steps
1. **Complete Authentication**: Implement JWT auth with user registration/login
2. **Database Setup**: Create and run initial migrations
3. **Add Minor Arcana**: Complete the tarot deck with all suits
4. **Partner CRUD**: Implement full partner management
5. **File Upload**: Add image upload for decks and personas
6. **Mobile App**: Start React Native client development

## 🧪 Testing

The project includes comprehensive tests for all core modules:

```bash
# Run all tests
make test

# Run specific test categories
cd backend
pytest tests/test_core.py -v          # Core calculation tests
pytest tests/ -k "astrology" -v       # Astrology tests only
pytest tests/ --cov=src --cov-report=html  # With coverage report
```

## 📚 API Endpoints

### Core Calculations
- `POST /api/v1/astro/chart` - Calculate birth chart
- `POST /api/v1/astro/compatibility` - Astrological compatibility
- `POST /api/v1/numerology/profile` - Complete numerology profile
- `POST /api/v1/zodiac/calculate` - Chinese zodiac calculation
- `POST /api/v1/tarot/draw` - Draw tarot cards

### Readings
- `POST /api/v1/readings/full` - Complete spiritual reading
- `GET /api/v1/readings/{id}` - Get reading results
- `POST /api/v1/readings/preview` - Preview reading (no save)

### Partners & Admin
- `GET /api/v1/partners/` - List partners
- `GET /api/v1/admin/earnings` - Revenue reports
- `GET /api/v1/admin/stats` - Platform statistics

## 🔧 Configuration

Key environment variables in `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://metamystic:password@localhost:5432/metamystic
REDIS_URL=redis://localhost:6379/0

# LLM Providers (configure at least one)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Security
JWT_SECRET=your-super-secret-jwt-key

# Storage (optional)
S3_BUCKET_NAME=metamystic-assets
S3_ACCESS_KEY_ID=your_access_key
```

## 🏗️ Architecture Overview

```
MetaMystic/
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── core/           # Pure calculation modules
│   │   │   ├── astro.py    # Astrology (Kerykeion)
│   │   │   ├── numerology.py
│   │   │   ├── tarot.py
│   │   │   └── zodiac.py
│   │   ├── services/       # Business logic
│   │   │   ├── ai/         # LLM providers
│   │   │   └── reading_service.py
│   │   ├── models/         # SQLAlchemy models
│   │   ├── api/           # FastAPI routes
│   │   └── schemas/       # Pydantic schemas
│   ├── tests/             # Test suite
│   └── alembic/           # Database migrations
├── data/                  # Static data files
│   ├── decks/            # Tarot deck definitions
│   └── spreads/          # Tarot spread layouts
├── partners/             # Partner-specific assets
├── scripts/              # Development scripts
└── mobile/              # React Native app (TODO)
```

## 🤝 Contributing

1. Follow PEP 8 style guidelines
2. Keep files under 300 lines
3. Maintain 90% test coverage on core modules
4. Use conventional commit messages: `<feat|fix|refactor>: <scope> - <summary>`
5. Run tests before committing: `make test`
6. Format code: `make format`

## 📄 License

Proprietary - All rights reserved

---

**Built with ❤️ for spiritual seekers and practitioners worldwide** 🔮✨
