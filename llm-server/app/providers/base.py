from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, *, system_prompt: str, user_prompt: str, model: str) -> str:
        raise NotImplementedError
