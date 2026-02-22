"""Backward compatibility import for the FastAPI file server."""

from chatapp.infrastructure.http.file_server import app, create_file_server

__all__ = ["app", "create_file_server"]
