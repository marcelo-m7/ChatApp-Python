"""Regras de validação e classificação de arquivos."""

from __future__ import annotations

import os

ALLOWED_EXTENSIONS: set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
}

IMAGE_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg", ".gif"}


def get_extension(file_name: str) -> str:
    return os.path.splitext(file_name)[1].lower()


def validate_allowed_extension(file_name: str) -> None:
    if get_extension(file_name) not in ALLOWED_EXTENSIONS:
        raise ValueError("Tipo de arquivo não permitido")


def is_image_file(file_name: str) -> bool:
    return get_extension(file_name) in IMAGE_EXTENSIONS

