from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIR = "src/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
UPLOAD_DIR_PATH = Path(UPLOAD_DIR).resolve()


def build_safe_upload_path(filename: str) -> tuple[str, Path]:
    decoded_name = unquote(filename)
    normalized_name = os.path.normpath(decoded_name)
    candidate_path = Path(normalized_name)

    if candidate_path.is_absolute() or ".." in candidate_path.parts:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    safe_name = str(candidate_path)
    final_path = (Path(UPLOAD_DIR) / safe_name).resolve()

    if UPLOAD_DIR_PATH not in final_path.parents and final_path != UPLOAD_DIR_PATH:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    return safe_name, final_path

@app.get("/download/{filename:path}")
async def download_file(filename: str):
    """Endpoint para baixar arquivos da pasta uploads"""
    safe_name, file_path = build_safe_upload_path(filename)

    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path, media_type="application/octet-stream", filename=safe_name)
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("SERVER_PORT", 3000))
    host = os.getenv("SERVER_HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port)
