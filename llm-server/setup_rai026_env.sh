#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KERNEL_NAME="rai026"
KERNEL_DISPLAY_NAME="Python (rai026)"
REBUILD_KERNEL=false

if [[ "${1:-}" == "--rebuild-kernel" ]]; then
  REBUILD_KERNEL=true
elif [[ "${1:-}" != "" ]]; then
  echo "Usage: $0 [--rebuild-kernel]"
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is not installed or not in PATH."
  echo "Install it from: https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

cd "${SCRIPT_DIR}"

# Create/update local .venv from lockfile with all optional extras.
uv sync --frozen --all-extras

# Register a reusable Jupyter kernel visible to all notebooks for this user.
if [[ "${REBUILD_KERNEL}" == "true" ]]; then
  uv run jupyter kernelspec remove -f "${KERNEL_NAME}" >/dev/null 2>&1 || true
fi
uv run python -m ipykernel install --user --name "${KERNEL_NAME}" --display-name "${KERNEL_DISPLAY_NAME}"

echo ""
echo "Environment ready via uv."
echo "Virtual environment: ${SCRIPT_DIR}/.venv"
echo "In Jupyter/VS Code, choose kernel: ${KERNEL_DISPLAY_NAME}"
