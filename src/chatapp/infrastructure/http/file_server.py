from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from chatapp.config.settings import settings
from chatapp.infrastructure.filename_utils import normalize_filename


def create_file_server(upload_dir: str | None = None) -> FastAPI:
    app = FastAPI()
    configured_upload_dir = upload_dir or settings.file_server_upload_dir
    os.makedirs(configured_upload_dir, exist_ok=True)

    @app.get("/download/{filename}")
    async def download_file(filename: str):
        """Download files from the configured uploads folder."""
        normalized_filename = normalize_filename(filename)
        file_path = os.path.join(configured_upload_dir, normalized_filename)

        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                media_type="application/octet-stream",
                filename=normalized_filename,
            )
        return {"error": "Arquivo não encontrado"}

    return app


app = create_file_server()
