# 🚀 MusicMood Quick Start Guide

Get MusicMood running in under 5 minutes!

## Prerequisites

- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- ✅ [Spotify Developer Account](https://developer.spotify.com/dashboard) (free)

## Step-by-Step Setup

### 1. Get Spotify Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create App"
3. Fill in app name and description
4. Copy your **Client ID** and **Client Secret**

### 2. Clone & Configure

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/MusicMood.git
cd MusicMood

# Copy environment template
cp .env.example .env
```

### 3. Add Your API Credentials

Edit `.env` file and add your Spotify credentials:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

> 💡 **Tip**: The `.env` file is gitignored - your secrets are safe!

### 4. Start Everything

**Windows:**
```powershell
.\start-app.ps1 start
```

**Linux/Mac:**
```bash
docker-compose up -d
```

### 5. Wait for Services to Start

The script will:
- 🐳 Pull Docker images (~2-3 min)
- 🤖 Download AI model (3.3GB, ~3-5 min first time)
- 🔧 Start 5 containers
- 🏥 Check health status
- ✅ Tell you when ready!

### 6. Access the App

Once you see "✅ All services are healthy!":

- **🎵 Web App**: http://localhost:8501
- **📚 API Docs**: http://localhost:8001/docs
- **🏥 Health Check**: http://localhost:8001/health

## 🎯 Generate Your First Playlist

1. Open http://localhost:8501
2. Enter your mood:
   - "I'm feeling happy and energetic"
   - "Relaxing mood for studying"
   - "Sad and reflective"
3. Click "Generate Playlist"
4. Wait ~30 seconds (AI is thinking!)
5. Enjoy your personalized playlist! 🎵

## 🛠️ Common Commands

```powershell
# Check status
.\start-app.ps1 status

# Stop everything
.\start-app.ps1 stop

# Restart
.\start-app.ps1 restart

# View logs
.\start-app.ps1 logs

# Get help
.\start-app.ps1 help
```

## 🐛 Troubleshooting

### Docker Not Running
```
Error: Cannot connect to Docker daemon
```
**Solution**: Make sure Docker Desktop is running

### Port Already in Use
```
Error: Port 8501 already in use
```
**Solution**: Stop other apps using ports 8001, 8501, 5433, 6380, 11434

### AI Model Download Slow
```
Downloading model... (3.3GB)
```
**Solution**: Be patient on first run. Subsequent starts are instant!

### API Credentials Invalid
```
Error: Invalid Spotify credentials
```
**Solution**: Double-check your Client ID and Secret in `.env`

## 📊 What's Running?

After successful startup:

| Service | Port | Purpose |
|---------|------|---------|
| **Frontend** | 8501 | Streamlit web interface |
| **Backend** | 8001 | FastAPI REST API |
| **PostgreSQL** | 5433 | Database (persistent data) |
| **Redis** | 6380 | Cache (fast responses) |
| **Ollama** | 11434 | Local AI model server |

## 🎓 Next Steps

- 📖 Read the [SETUP_GUIDE.md](SETUP_GUIDE.md) for architecture details
- 🐳 Check [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for Docker tips
- 🔧 Explore [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for deployment
- 💻 Browse the API docs at http://localhost:8001/docs

## 🆘 Need Help?

- Check logs: `.\start-app.ps1 logs`
- Verify health: http://localhost:8001/health
- Review [DOCKER_GUIDE.md](DOCKER_GUIDE.md) troubleshooting section

---

**Happy Music Discovery! 🎵✨**
