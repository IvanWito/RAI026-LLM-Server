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

## Setup
1. First-time only (creates lockfile):
```bash
cd llm-server
uv lock
```
2. Create/update environment and Jupyter kernel:
```bash
./setup_rai026_env.sh
```

What the script does:
- Runs `uv sync --frozen --all-extras` inside `llm-server`.
- Installs/updates Jupyter kernel `Python (rai026)` for user scope.

If kernel selection breaks after env changes:
```bash
./llm-server/setup_rai026_env.sh --rebuild-kernel
```

## Devcontainer (Recommended For Team Dev)
Open `llm-server` with VS Code Dev Containers:
1. `Dev Containers: Open Folder in Container...`
2. Select `llm-server`
3. Wait for `postCreateCommand` (`uv sync --all-extras`) to finish

The container definition is in:
- `.devcontainer/devcontainer.json`
- `.devcontainer/Dockerfile`

## Run Server
1. Create env file:
```bash
cp .env.example llm-server/.env
```
2. Start Ollama and pull the model configured in `.env` (default in example: `phi4:14b`):
```bash
ollama serve
ollama pull phi4:14b
```
3. Start API:
```bash
cd llm-server
./run.sh
```

For local development auto-reload:
```bash
cd llm-server
RELOAD=true ./run.sh
```

## Remote Serving For Robot Access
Run the server on an online machine with a public/reachable IP.

1. Configure `.env`:
```bash
HOST=0.0.0.0
PORT=8000
SERVER_API_KEY=change_this_to_a_strong_secret
CORS_ALLOW_ORIGINS=https://your-ui-domain.com,http://your-robot-gateway.local
```
2. Start server (no reload, production-like):
```bash
cd llm-server
./run.sh
```
3. Open firewall/security group for TCP `8000` (or use a reverse proxy like Nginx/Caddy).
4. Robot calls must include header:
```http
X-API-Key: <SERVER_API_KEY>
```

## Quick Checks
Health:
```bash
curl http://localhost:8000/health
```

Process:
```bash
curl -X POST http://localhost:8000/v1/process \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change_this_to_a_strong_secret' \
  -d '{
    "transcript": "please move forward slowly for one meter",
    "context": {"battery": 0.84, "obstacle_detected": false},
    "history": []
  }'
```

## Model Configuration Note
- `.env.example` currently sets `LLM_MODEL=phi4:14b`.
- Code default in `app/config.py` is `llama3.1:8b`.
- Runtime uses `.env` if present, so `.env` value has priority.
