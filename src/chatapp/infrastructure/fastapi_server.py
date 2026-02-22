from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from chatapp.config.settings import settings
from chatapp.infrastructure.filename_utils import normalize_filename

app = FastAPI()

os.makedirs(settings.server_upload_dir, exist_ok=True)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download files from uploads folder."""
    normalized_filename = normalize_filename(filename)
    file_path = os.path.join(settings.server_upload_dir, normalized_filename)

    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=normalized_filename,
        )
    return {"error": "Arquivo não encontrado"}
