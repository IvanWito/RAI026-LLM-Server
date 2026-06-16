from __future__ import annotations

from app.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str | None, timeout_seconds: float = 30.0):
        self.api_key = api_key
        self.timeout = timeout_seconds

    async def generate(self, *, system_prompt: str, user_prompt: str, model: str) -> str:
        raise NotImplementedError(
            "Gemini provider not wired yet. Add SDK/REST call here once API key/model choice is finalized."
        )
