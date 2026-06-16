#!/usr/bin/env bash
set -euo pipefail

UVICORN_ARGS=(app.main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}")

if [[ "${RELOAD:-false}" == "true" ]]; then
  UVICORN_ARGS+=(--reload)
fi

uv run uvicorn "${UVICORN_ARGS[@]}"
