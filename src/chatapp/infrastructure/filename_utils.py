"""Utilities for filename normalization."""

from urllib.parse import unquote


def normalize_filename(raw_name: str) -> str:
    """Decode URL-encoded names and normalize spaces."""
    decoded = unquote(raw_name)
    return decoded.replace("%", " ")
