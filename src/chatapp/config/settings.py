"""Centralized runtime settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "localhost")
    port: int = int(os.getenv("PORT", "8550"))
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads/")
    assets_dir: str = os.getenv("ASSETS_DIR", "assets")

    file_server_host: str = os.getenv("FILE_SERVER_HOST", os.getenv("SERVER_HOST", "0.0.0.0"))
    file_server_port: int = int(os.getenv("FILE_SERVER_PORT", os.getenv("SERVER_PORT", "3000")))
    file_server_upload_dir: str = os.getenv("FILE_SERVER_UPLOAD_DIR", os.getenv("SERVER_UPLOAD_DIR", "src/uploads"))
    file_server_download_url_template: str = os.getenv(
        "FILE_SERVER_DOWNLOAD_URL_TEMPLATE",
        "http://127.0.0.1:3000/download/{filename}",
    )

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    assistant_model: str = os.getenv("ASSISTANT_MODEL", "gpt-3.5-turbo")
    assistant_temperature: float = float(os.getenv("ASSISTANT_TEMPERATURE", "0.7"))
    assistant_name: str = os.getenv("ASSISTANT_NAME", "Programador")

    github_client_id: str | None = os.getenv("GITHUB_CLIENT_ID")
    github_client_secret: str | None = os.getenv("GITHUB_CLIENT_SECRET")
    github_redirect_url: str = os.getenv("GITHUB_REDIRECT_URL", "http://localhost:8550/oauth_callback")


settings = Settings()
