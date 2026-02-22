"""Centralized runtime settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "localhost")
    port: int = int(os.getenv("PORT", "8550"))
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "3000"))
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads/")
    server_upload_dir: str = os.getenv("SERVER_UPLOAD_DIR", "src/uploads")
    assets_dir: str = os.getenv("ASSETS_DIR", "assets")


settings = Settings()
