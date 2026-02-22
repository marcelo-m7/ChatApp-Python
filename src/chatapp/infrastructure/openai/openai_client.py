from __future__ import annotations

from openai import OpenAI

from chatapp.config.settings import settings


def create_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)
