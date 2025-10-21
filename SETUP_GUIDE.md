# Phase 1 Setup Guide - Complete Installation Instructions

This guide will walk you through completing Phase 1 of the MusicMood project setup.

## ✅ Task 1.5: Python Environment - COMPLETED

- [x] Poetry environment created
- [x] All dependencies installed (123 packages)
- [x] All imports verified successfully
- [x] Project structure created

## 📋 Remaining Tasks

### Task 1.1: Ollama Local LLM Setup

#### Subtask 1.1.1: Install Ollama

**Windows Installation:**
1. Visit: https://ollama.ai/download/windows
2. Download OllamaSetup.exe
3. Run the installer
4. Ollama will start as a Windows service automatically

**Verification:**
```powershell
# Check Ollama is running
curl http://localhost:11434

# Should return: "Ollama is running"
```

#### Subtask 1.1.2: Download Mistral Model

```powershell
# Pull Mistral 7B model (~4GB download)
ollama pull mistral

# Verify model is downloaded
ollama list

# Expected output should show: mistral:latest
```

#### Subtask 1.1.3: Test Ollama API

```powershell
# Test with simple prompt
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "What is AI?",
  "stream": false
}'

# Should return JSON with response field
```

**Verification Checklist:**
- [ ] Ollama running on localhost:11434
- [ ] Mistral model downloaded (ollama list shows it)
- [ ] API responds to generate endpoint
- [ ] Response contains coherent text

---

### Task 1.2: PostgreSQL Database Setup

#### Subtask 1.2.1: Install PostgreSQL

**Windows Installation:**
1. Download: https://www.postgresql.org/download/windows/
2. Run the installer (PostgreSQL 15 or higher)
3. Set admin password during installation (remember this!)
4. Keep default port: 5432
5. Ensure PostgreSQL service starts automatically

**Verification:**
```powershell
# Check PostgreSQL version
psql --version

# Should show: psql (PostgreSQL) 15.x or higher
```

#### Subtask 1.2.2: Create Database and User

```powershell
# Connect to PostgreSQL as admin
psql -U postgres

# In psql prompt, run:
```

```sql
-- Create application user
CREATE USER musicmood_user WITH PASSWORD 'musicmood_pass';

-- Create database
CREATE DATABASE musicmood OWNER musicmood_user;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE musicmood TO musicmood_user;

-- Connect to new database
\c musicmood

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO musicmood_user;

-- Exit psql
\q
```

#### Subtask 1.2.3: Test Connection

```powershell
# Test connection with new user
psql -U musicmood_user -d musicmood -h localhost

# In psql prompt, test operations:
```

```sql
-- Create test table
CREATE TABLE test (id SERIAL PRIMARY KEY, name VARCHAR(100));

-- Insert data
INSERT INTO test (name) VALUES ('test1');

-- Query data
SELECT * FROM test;

-- Drop test table
DROP TABLE test;

-- Exit
\q
```

**Verification Checklist:**
- [ ] PostgreSQL service running
- [ ] Can connect as postgres user
- [ ] musicmood database created
- [ ] musicmood_user created with password
- [ ] User can perform CRUD operations
- [ ] Connection string works: `postgresql://musicmood_user:musicmood_pass@localhost:5432/musicmood`

---

### Task 1.3: Redis Cache Setup

#### Subtask 1.3.1: Install Redis

**Windows Installation:**
1. Redis doesn't have official Windows builds. Use WSL or Docker:

**Option 1: Using Docker (Recommended)**
```powershell
# Install Docker Desktop first if not installed
# Then run Redis container:
docker run -d --name redis-musicmood -p 6379:6379 redis:7-alpine

# Verify Redis is running
docker ps
```

**Option 2: Using WSL**
```bash
# In WSL terminal:
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

#### Subtask 1.3.2: Configure Redis

**If using Docker:**
```powershell
# Create redis.conf file
# Run Redis with config:
docker run -d --name redis-musicmood -p 6379:6379 -v ${PWD}/redis.conf:/usr/local/etc/redis/redis.conf redis:7-alpine redis-server /usr/local/etc/redis/redis.conf
```

**redis.conf minimal settings:**
```
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### Subtask 1.3.3: Test Redis

```powershell
# Using redis-cli (install via Docker)
docker exec -it redis-musicmood redis-cli

# In redis-cli, test operations:
```

```redis
# Set a key
SET test_key "Hello Redis"

# Get the key
GET test_key

# Set with expiration (10 seconds)
SETEX temp_key 10 "Temporary value"

# Wait 10 seconds then get (should be nil)
GET temp_key

# Test list operations
LPUSH mylist "item1"
LPUSH mylist "item2"
LRANGE mylist 0 -1

# Exit
exit
```

**Or test with Python:**
```powershell
poetry run python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); r.set('test', 'works'); print('Redis working:', r.get('test'))"
```

**Verification Checklist:**
- [ ] Redis running on port 6379
- [ ] Can connect via redis-cli or Python
- [ ] SET/GET operations work
- [ ] Expiration works (SETEX)
- [ ] List/Hash operations work
- [ ] maxmemory configured (512mb)

---

### Task 1.4: API Keys & Credentials Setup

#### Subtask 1.4.1: Spotify API Credentials

1. **Create Spotify Developer Account:**
   - Visit: https://developer.spotify.com/dashboard
   - Log in with Spotify account (or create one)
   - Accept Terms of Service

2. **Create New App:**
   - Click "Create App"
   - App name: "MusicMood Dev"
   - App description: "Mood-based music recommendation system"
   - Redirect URI: `http://localhost:8000/callback`
   - Check Web API
   - Click "Create"

3. **Get Credentials:**
   - Click "Settings"
   - Copy **Client ID**
   - Click "View client secret"
   - Copy **Client Secret**

4. **Update .env file:**
```env
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
```

#### Subtask 1.4.2: OpenWeatherMap API Key

1. **Create Account:**
   - Visit: https://openweathermap.org/api
   - Click "Sign Up"
   - Verify email

2. **Get API Key:**
   - Log in to dashboard
   - Navigate to "API keys" section
   - Copy your default API key (or generate new one)
   - Note: Free tier allows 1000 calls/day

3. **Update .env file:**
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

#### Subtask 1.4.3: Verify .env File

Your final `.env` file should look like:

```env
# Application
APP_NAME=MusicMood
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://musicmood_user:musicmood_pass@localhost:5432/musicmood

# Redis
REDIS_URL=redis://localhost:6379/0

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Spotify API (FILLED IN)
SPOTIFY_CLIENT_ID=abc123xyz789... (your actual ID)
SPOTIFY_CLIENT_SECRET=def456uvw012... (your actual secret)

# OpenWeatherMap (FILLED IN)
OPENWEATHER_API_KEY=ghi789rst345... (your actual key)
```

**Verification Checklist:**
- [ ] Spotify app created in developer dashboard
- [ ] Client ID copied to .env
- [ ] Client Secret copied to .env
- [ ] OpenWeatherMap account created
- [ ] API key copied to .env
- [ ] .env file has all values filled
- [ ] .env is in .gitignore (never commit!)

---

## 🧪 Final Phase 1 Verification

After completing all tasks above, run the verification script:

```powershell
# Verify all services
poetry run python verify_phase1.py
```

This script will check:
1. ✓ Ollama is running and responds
2. ✓ Mistral model is available
3. ✓ PostgreSQL connection works
4. ✓ Database user has proper permissions
5. ✓ Redis connection works
6. ✓ Redis operations functional
7. ✓ Spotify credentials valid
8. ✓ OpenWeather API key valid
9. ✓ All environment variables set

## 📝 Phase 1 Completion Checklist

Before moving to Phase 2, verify:

**Ollama Services:**
- [ ] Ollama running on localhost:11434
- [ ] Mistral model loaded and responsive
- [ ] API endpoint tested and working

**Database Services:**
- [ ] PostgreSQL running on port 5432
- [ ] musicmood database created
- [ ] Application user with full privileges
- [ ] Connection string works

**Cache Services:**
- [ ] Redis running on port 6379
- [ ] Redis operations (SET/GET/DEL) working
- [ ] Memory configuration applied

**Credentials:**
- [ ] Spotify API credentials obtained
- [ ] OpenWeatherMap API key obtained
- [ ] .env file updated with all secrets
- [ ] .env not tracked by git

**Python Environment:**
- [ ] Virtual environment active and working
- [ ] All dependencies installed (123 packages)
- [ ] All imports successful
- [ ] Test script runs without errors

## ✅ Status

Once all checkboxes are checked, you're ready to move to **Phase 2: Core Backend Architecture & Database Models**!

---

**Need Help?**
- Ollama docs: https://ollama.ai/docs
- PostgreSQL docs: https://www.postgresql.org/docs/
- Redis docs: https://redis.io/docs/
- Spotify API docs: https://developer.spotify.com/documentation/web-api
