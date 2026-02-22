"""Utilities for filename normalization."""

from pathlib import Path
from urllib.parse import unquote


def normalize_filename(raw_name: str) -> str:
    """Decode URL-encoded names and strip directory traversal."""
    decoded = unquote(raw_name).strip()
    return Path(decoded).name
