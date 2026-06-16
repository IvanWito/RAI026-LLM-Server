from __future__ import annotations

from app.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str | None, base_url: str, timeout_seconds: float = 30.0):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout_seconds

    async def generate(self, *, system_prompt: str, user_prompt: str, model: str) -> str:
        raise NotImplementedError(
            "OpenAI provider not wired yet. Add SDK call here once API key/model choice is finalized."
        )
