from __future__ import annotations

import json
from typing import Type, TypeVar

import httpx
from pydantic import BaseModel

from support_agent.config import settings

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    def __init__(self) -> None:
        self.provider = settings.provider
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.base_url = settings.openrouter_base_url

    async def complete_text(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert customer support AI. "
                        "Follow instructions exactly. If JSON is requested, return only valid JSON."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    async def complete_json(self, prompt: str, schema: Type[T]) -> T:
        text = await self.complete_text(prompt)
        cleaned = text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1).replace("```", "").strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "").strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            parsed = json.loads(self._extract_json_block(cleaned))

        return schema.model_validate(parsed)

    def _extract_json_block(self, text: str) -> str:
        start_obj = text.find("{")
        end_obj = text.rfind("}")
        if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
            return text[start_obj:end_obj + 1]

        start_arr = text.find("[")
        end_arr = text.rfind("]")
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            return text[start_arr:end_arr + 1]

        raise ValueError(f"Could not parse JSON from model output:\n{text}")