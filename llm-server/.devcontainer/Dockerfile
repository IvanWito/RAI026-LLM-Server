FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Install uv for dependency management (globally available for non-root user).
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

WORKDIR /workspaces/R-AI-026/llm-server
