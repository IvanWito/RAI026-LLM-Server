# LLM Server MVP (Robot Brain)

This service receives a speech-to-text transcript, asks an LLM for a single robot instruction, and returns structured JSON for your orchestrator.

## Current Functionality
- FastAPI server with `GET /health` and `POST /v1/process`.
- Provider abstraction with `ollama` active now.
- `openai` and `gemini` provider stubs ready to wire.
- Notebook smoke test at `notebooks/smoke_test.ipynb`.

## Project Files
- `app/main.py` - routes and API entrypoint.
- `app/models.py` - request/response schemas.
- `app/services.py` - prompt building and output parsing.
- `app/providers/` - provider implementations.
- `app/prompts/system_prompt.txt` - safety/system prompt.
- `setup_rai026_env.sh` - env + kernel setup script.

## Install Server

### Prerequisites
- Docker and Docker Compose installed on your server
- Ollama installed for LLM inference

### Step 1: Clone the repository
```bash
cd ~
git clone <URL-del-repo> rai026-llm-server
cd rai026-llm-server/llm-server
```

### Step 2: Install Docker Compose (if not already installed)
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

### Step 3: Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sudo bash
ollama version
```

### Step 4: Configure environment variables
```bash
cp .env.example .env
nano .env
```

Update these key variables:
- `SERVER_API_KEY=your_secure_api_key`
- `LLM_MODEL=phi4:14b` (or your preferred model)
- `OLLAMA_BASE_URL=http://localhost:11434`

### Step 5: Download Ollama model
```bash
ollama pull phi4:14b
```

Replace `phi4:14b` with your configured model from `.env`.

---

## Run

### Starting the Services

#### 1) Start Ollama (in background or separate terminal)
```bash
ollama serve &
```

#### 2) Build and start the LLM Server with Docker Compose
From `llm-server/` directory:
```bash
cd ~/rai026-llm-server/llm-server
docker-compose up -d --build
```

This will:
- Build the Docker image using `.devcontainer/Dockerfile`
- Mount your code volume
- Load environment variables from `.env`
- Install dependencies with `uv sync --all-extras`
- Start the FastAPI server on port 8000

### Monitoring

Check if containers are running:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

### Testing the Server

Health check:
```bash
curl http://localhost:8000/health
```

Process endpoint:
```bash
curl -X POST http://localhost:8000/v1/process \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secure_api_key" \
  -d '{
    "transcript": "please move forward slowly for one meter",
    "context": {"battery": 0.84, "obstacle_detected": false},
    "history": []
  }'
```

### Stopping the Server

```bash
docker-compose down
```

---

## Local Development (with auto-reload)

### Using Dev Containers in VS Code
1. Open `llm-server` folder in VS Code
2. Run `Dev Containers: Open Folder in Container...`
3. Wait for `postCreateCommand` to complete
4. Start API with auto-reload:
```bash
RELOAD=true ./run.sh
```

### Or using uv directly (without Docker)
```bash
cd llm-server
uv lock
uv sync --all-extras
RELOAD=true ./run.sh
```

---

## Remote Serving For Robot Access

Configure for production deployment:

1. Update `.env`:
```bash
HOST=0.0.0.0
PORT=8000
SERVER_API_KEY=change_this_to_a_strong_secret
CORS_ALLOW_ORIGINS=https://your-ui-domain.com,http://your-robot-gateway.local
```

2. Open firewall for TCP 8000 (or use reverse proxy):
```bash
sudo ufw allow 8000/tcp
```

3. Robot requests must include header:
```http
X-API-Key: <SERVER_API_KEY>
```

---

## Model Configuration Note
- `.env.example` currently sets `LLM_MODEL=phi4:14b`.
- Code default in `app/config.py` is `llama3.1:8b`.
- Runtime uses `.env` if present, so `.env` value has priority.
