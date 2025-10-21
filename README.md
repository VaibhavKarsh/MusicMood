# MusicMood 🎵🧠

**A Production-Grade 3-Agent AI System for Mood-Based Music Recommendations**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

MusicMood is an intelligent music recommendation system that uses a **multi-agent AI architecture** to understand user moods and generate personalized Spotify playlists. The system employs three specialized AI agents working sequentially to analyze mood, discover music, and curate the perfect playlist.

### Key Features

- **🤖 3-Agent AI Architecture**: Specialized agents for mood understanding, music discovery, and playlist curation
- **🧰 8 LangChain Tools**: Custom tools distributed across agents (2+3+3) for intelligent reasoning
- **🧠 ReAct Pattern**: Agents use reasoning and action loops for transparent decision-making
- **🎸 Spotify Integration**: Real-time music search and audio feature analysis
- **💾 Intelligent Caching**: Redis-based caching for optimal performance
- **📊 User Personalization**: Historical mood tracking and preference learning
- **⚡ Fast Performance**: Complete pipeline executes in <10 seconds

## 🏗️ Architecture

### Multi-Agent Pipeline

```
User Input ("I'm feeling happy and energetic")
    ↓
┌─────────────────────────────────────────┐
│  Agent 1: Mood Understanding Agent      │
│  Tools: parse_mood_with_llm,            │
│         get_user_context                │
│  Output: mood_data                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Agent 2: Music Discovery Agent         │
│  Tools: search_spotify_by_mood,         │
│         get_audio_features_batch,       │
│         filter_tracks_by_criteria       │
│  Output: 50+ candidate_tracks           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Agent 3: Playlist Curator Agent        │
│  Tools: rank_tracks_by_relevance,       │
│         optimize_diversity,             │
│         generate_explanation            │
│  Output: 30-track final_playlist        │
└─────────────────────────────────────────┘
    ↓
Final Playlist + Explanation
```

### Technology Stack

**AI/ML Layer:**
- **Ollama + Mistral 7B**: Local LLM for mood understanding and reasoning
- **LangChain**: Agent framework with ReAct pattern implementation
- **Sentence Transformers**: Mood embeddings for similarity matching

**Backend:**
- **FastAPI**: High-performance REST API
- **SQLAlchemy**: ORM for PostgreSQL database
- **Redis**: Caching layer for performance optimization
- **Pydantic**: Data validation and settings management

**APIs:**
- **Spotify Web API**: Music search and audio feature analysis
- **OpenWeatherMap API**: Weather context for mood enhancement

**Frontend:**
- **Streamlit**: Interactive web interface for playlist generation

**Deployment:**
- **Docker**: Containerization for all services
- **GitHub Actions**: CI/CD pipeline
- **Railway/Streamlit Cloud**: Production hosting

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.11+** installed
2. **Poetry** for dependency management
3. **PostgreSQL 15+** running locally
4. **Redis 7+** running locally
5. **Ollama** installed with Mistral model
6. **Spotify Developer Account** (for API credentials)
7. **OpenWeatherMap Account** (for API key)

## 🚀 Quick Start

### 1. Clone and Setup Environment

```powershell
# Navigate to project directory
cd e:\Portfolio\MusicMood

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell
```

### 2. Configure Environment Variables

```powershell
# Copy example env file
cp .env.example .env

# Edit .env and add your API credentials:
# - SPOTIFY_CLIENT_ID
# - SPOTIFY_CLIENT_SECRET
# - OPENWEATHER_API_KEY
```

### 3. Start Required Services

```powershell
# Start Ollama (in separate terminal)
ollama serve

# Pull Mistral model
ollama pull mistral

# Start PostgreSQL (should be running as service)
# Start Redis (should be running as service)
```

### 4. Initialize Database

```powershell
# Run database migrations
poetry run alembic upgrade head
```

### 5. Start the Application

```powershell
# Start FastAPI backend
poetry run uvicorn app.main:app --reload --port 8000

# In another terminal, start Streamlit frontend
poetry run streamlit run app/frontend/streamlit_app.py
```

### 6. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501
- **Health Check**: http://localhost:8000/api/health

## 📁 Project Structure

```
MusicMood/
├── app/
│   ├── agents/              # 3 AI Agents
│   │   ├── mood_agent.py           # Agent 1: Mood Understanding
│   │   ├── discovery_agent.py      # Agent 2: Music Discovery
│   │   └── curator_agent.py        # Agent 3: Playlist Curator
│   ├── tools/               # 8 LangChain Tools
│   │   ├── mood_tools.py           # Tools 1-2 for Agent 1
│   │   ├── spotify_tools.py        # Tools 3-5 for Agent 2
│   │   └── curator_tools.py        # Tools 6-8 for Agent 3
│   ├── models/              # Database Models
│   │   ├── user.py
│   │   ├── mood.py
│   │   └── playlist.py
│   ├── services/            # Business Logic
│   │   ├── spotify/
│   │   │   └── spotify_client.py
│   │   ├── orchestrator.py         # Multi-agent orchestration
│   │   └── database.py
│   ├── routes/              # API Endpoints
│   │   ├── health.py
│   │   └── playlist.py
│   ├── config/              # Configuration
│   │   └── settings.py
│   └── main.py              # FastAPI Application
├── tests/                   # Test Suite
├── docker-compose.yml       # Docker Services
├── pyproject.toml           # Poetry Dependencies
└── README.md                # This file
```

## 🧪 Testing

```powershell
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_agents.py

# Test imports
poetry run python test_imports.py
```

## 📊 Performance Benchmarks

| Metric | Target | Actual |
|--------|--------|--------|
| Agent 1 Latency | <2s | TBD |
| Agent 2 Latency | <5s | TBD |
| Agent 3 Latency | <2s | TBD |
| End-to-End Pipeline | <10s | TBD |
| Cache Hit Latency | <500ms | TBD |
| Mood Parsing Accuracy | >90% | TBD |
| Track Filtering Accuracy | >85% | TBD |
| Ranking Relevance | >80% | TBD |

## 🔧 Development Workflow

### Phase 1: Environment Setup ✅
- [x] Poetry environment created
- [x] All dependencies installed
- [x] Project structure created
- [x] Configuration files set up
- [ ] Ollama configured
- [ ] PostgreSQL configured
- [ ] Redis configured
- [ ] API credentials obtained

### Phase 2: Backend Architecture (In Progress)
- [ ] FastAPI application initialized
- [ ] Database models created
- [ ] Database migrations set up
- [ ] Health check endpoint

### Phase 3-5: Agent Implementation
- [ ] Agent 1: Mood Understanding
- [ ] Agent 2: Music Discovery
- [ ] Agent 3: Playlist Curator
- [ ] Multi-agent orchestration

### Phase 6-7: Frontend & Containerization
- [ ] Streamlit UI
- [ ] Docker setup
- [ ] Local testing

### Phase 8-10: Deployment
- [ ] CI/CD pipeline
- [ ] Cloud deployment
- [ ] Documentation

## 🤝 Contributing

This is a portfolio project. For suggestions or issues:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for the agent framework
- **Ollama** for local LLM capabilities
- **Spotify** for comprehensive music API
- **FastAPI** for the excellent web framework

## 📞 Contact

**Portfolio Project for Mrsool Interview**

- GitHub: [Your GitHub Profile]
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

---

**Built with ❤️ using LangChain, FastAPI, and Ollama**
