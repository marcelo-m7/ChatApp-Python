from pathlib import Path, PurePosixPath, PureWindowsPath

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIR = "src/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint para baixar arquivos da pasta uploads"""
    if not filename:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    if "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    filename_path = Path(filename)
    if (
        filename_path.is_absolute()
        or PurePosixPath(filename).is_absolute()
        or PureWindowsPath(filename).is_absolute()
        or ".." in filename_path.parts
        or filename_path.name != filename
    ):
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido")

    upload_dir = Path(UPLOAD_DIR).resolve()
    file_path = (upload_dir / filename_path.name).resolve()

    try:
        file_path.relative_to(upload_dir)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido") from exc

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename_path.name)

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("SERVER_PORT", 3000))
    host = os.getenv("SERVER_HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port)
