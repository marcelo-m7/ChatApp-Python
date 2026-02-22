from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


client = TestClient(server.app)


def test_download_valid_filename_returns_file(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    target = upload_dir / "example.txt"
    target.write_text("content", encoding="utf-8")

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))

    response = client.get("/download/example.txt")

    assert response.status_code == 200
    assert response.content == b"content"
    assert response.headers["content-disposition"].startswith('attachment; filename="example.txt"')


def test_download_nonexistent_file_returns_404(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))

    response = client.get("/download/missing.txt")

    assert response.status_code == 404
    assert response.json() == {"detail": "Arquivo não encontrado"}


def test_download_rejects_dotdot_with_backslash(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))

    response = client.get(r"/download/..\\secret.txt")

    assert response.status_code == 400
    assert response.json() == {"detail": "Nome de arquivo inválido"}


def test_download_rejects_path_separator(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))

    response = client.get(r"/download/folder\\file.txt")

    assert response.status_code == 400
    assert response.json() == {"detail": "Nome de arquivo inválido"}


def test_download_rejects_absolute_windows_style_path(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))

    response = client.get(r"/download/C:\\temp\\secret.txt")

    assert response.status_code == 400
    assert response.json() == {"detail": "Nome de arquivo inválido"}
