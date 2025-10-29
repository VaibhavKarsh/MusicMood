# MusicMood 🎵🧠

**An AI System for Mood-Based Music Recommendations**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://python.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

MusicMood is an intelligent music recommendation system that uses a **multi-agent AI architecture** to understand user moods and generate personalized Spotify playlists. The system employs three specialized AI agents working sequentially to analyze mood, discover music, and curate the perfect playlist.

### ✨ Key Features

- **🤖 3-Agent AI System**: Specialized agents working sequentially (Mood → Discovery → Curation)
- **🧰 8 Custom LangChain Tools**: Distributed across agents (2+3+3) for intelligent reasoning
- **🧠 Local AI (Ollama)**: Runs gemma3:4b model locally - no API costs!
- **🎸 Real Spotify Data**: Live music search with 50+ audio features per track
- **💾 Smart Caching**: Redis-based caching for instant repeat queries
- **📊 Mood History**: Track your mood journey and music preferences over time
- **🐳 Fully Dockerized**: One command to run everything - no complex setup
- **⚡ Production-Ready**: Complete with health checks and error handling

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
- **Ollama + Gemma 3 (4B)**: Local LLM for mood understanding and reasoning (no API costs!)
- **LangChain 0.3+**: Agent framework with ReAct pattern
- **Pydantic AI**: Structured outputs for reliability

**Backend:**
- **FastAPI 0.115+**: High-performance async REST API
- **SQLAlchemy 2.0**: Modern ORM with PostgreSQL 15
- **Redis 7**: Advanced caching with pub/sub
- **Alembic**: Database migrations

**APIs:**
- **Spotify Web API**: 50+ audio features per track, real-time search
- **Supports multiple models**: Ollama (local), Replicate, OpenAI

**Frontend:**
- **Streamlit 1.39+**: Clean, responsive UI with dark theme

**DevOps:**
- **Docker Compose**: 5 containers orchestrated (Backend, Frontend, DB, Cache, AI)
- **GitHub Actions**: 2 automated workflows (CI build + CD docker push)
- **Multi-stage Builds**: Optimized Docker images

## 📋 What You Need

**For Docker Setup (Recommended):**
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - That's it! Everything else runs in containers
- [Spotify Developer Account](https://developer.spotify.com/dashboard) - Free API credentials

**For Manual Setup (Advanced):**
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Ollama with gemma3:4b model

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- Spotify API credentials ([Get them here](https://developer.spotify.com/dashboard))

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/MusicMood.git
cd MusicMood
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Spotify credentials
# SPOTIFY_CLIENT_ID=your_client_id_here
# SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### 3. Start Everything with One Command! 🚀

```powershell
# Windows
.\start-app.ps1 start

# Linux/Mac
docker-compose up -d
```

That's it! The script will:
- ✅ Start all 5 Docker containers (Backend, Frontend, PostgreSQL, Redis, Ollama)
- ✅ Run database migrations automatically
- ✅ Download AI models (gemma3:4b - 3.3GB)
- ✅ Perform health checks
- ✅ Show you when everything is ready

### 4. Access the Application

Once you see "✅ All services are healthy!", open:

- **🎵 Web App**: http://localhost:8501
- **📚 API Docs**: http://localhost:8001/docs
- **🏥 Health Check**: http://localhost:8001/health

### 5. Generate Your First Playlist!

1. Open http://localhost:8501
2. Enter your mood (e.g., "I'm feeling happy and energetic!")
3. Click "Generate Playlist"
4. Wait ~30 seconds for AI magic ✨
5. Enjoy your personalized playlist!

## 🛠️ Management Commands

```powershell
# Check status of all services
.\start-app.ps1 status

# Stop all services
.\start-app.ps1 stop

# Restart everything
.\start-app.ps1 restart

# View live logs
.\start-app.ps1 logs

# Get help
.\start-app.ps1 help
```

## 💻 Manual Setup (Without Docker)

<details>
<summary>Click to expand manual setup instructions</summary>

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Ollama with gemma3:4b model

### Steps

1. **Install Dependencies**
   ```bash
   poetry install
   poetry shell
   ```

2. **Setup Database**
   ```bash
   alembic upgrade head
   ```

3. **Start Services**
   ```bash
   # Terminal 1: Backend
   uvicorn app.main:app --reload --port 8001
   
   # Terminal 2: Frontend
   streamlit run app/frontend/minimal_app.py
   ```

</details>

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

## 📊 Performance

| Metric | Performance |
|--------|-------------|
| **End-to-End Pipeline** | ~30 seconds (first run with local AI) |
| **Cache Hit Response** | <1 second |
| **Docker Startup** | ~30 seconds (all 5 containers healthy) |
| **AI Model Size** | 3.3GB (gemma3:4b) |
| **Memory Usage** | ~4GB total (all containers) |
| **Database Tables** | 4 (users, moods, playlists, tracks) |

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
- [x] Streamlit UI
- [x] Docker setup
- [x] Local testing

### Phase 8-10: Deployment & Production
- [x] CI/CD pipeline (GitHub Actions)
- [x] Docker containerization with Ollama
- [x] Production-ready configurations
- [ ] Cloud deployment (Render.com + Streamlit Cloud)
- [x] Comprehensive documentation

## 🎥 Demo Video

> Coming soon! Will include:
> - Quick setup demonstration
> - Playlist generation walkthrough
> - Architecture explanation
> - Performance benchmarks

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

## 📞 Connect

**Portfolio Project** showcasing production-grade AI engineering

- **GitHub**: [github.com/Vaibhav Karsh](https://github.com/VaibhavKarsh)
- **LinkedIn**: [linkedin.com/in/Vaibhav Karsh](https://linkedin.com/in/](https://www.linkedin.com/in/vaibhav-karsh-527479258/)

---

<div align="center">

**Built with ❤️ using LangChain, FastAPI, and Ollama**

⭐ Star this repo if you found it helpful!

</div>
