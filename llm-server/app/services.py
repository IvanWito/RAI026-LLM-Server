from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from app.config import settings
from app.models import BrainInstruction
from app.providers.base import LLMProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider


def get_provider(provider_name: str | None = None) -> LLMProvider:
    name = (provider_name or settings.llm_provider).lower()

    if name == "ollama":
        return OllamaProvider(settings.ollama_base_url, settings.request_timeout_seconds)
    if name == "openai":
        return OpenAIProvider(settings.openai_api_key, settings.openai_base_url, settings.request_timeout_seconds)
    if name == "gemini":
        return GeminiProvider(settings.gemini_api_key, settings.request_timeout_seconds)

    raise ValueError(f"Unsupported provider '{name}'")


def build_user_prompt(transcript: str, context: dict, history: list[dict]) -> str:
    payload = {
        "transcript": transcript,
        "context": context,
        "history": history,
    }
    return json.dumps(payload, ensure_ascii=True)


def load_system_prompt() -> str:
    prompt_path = Path(__file__).parent / "prompts" / "system_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")


def parse_instruction(raw_text: str) -> BrainInstruction:
    text = raw_text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        # raw_decode stops at the first valid JSON object, ignoring trailing text
        data, _ = json.JSONDecoder().raw_decode(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model output is not valid JSON: {exc} | raw={text[:300]!r}") from exc

    try:
        return BrainInstruction.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Model JSON does not match BrainInstruction schema: {exc} | raw={text[:300]!r}") from exc
