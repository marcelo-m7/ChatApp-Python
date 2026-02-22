from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import server


@pytest.fixture
def client(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(server, "UPLOAD_DIR_PATH", upload_dir.resolve())

    return TestClient(server.app), upload_dir


def test_download_file_success(client):
    test_client, upload_dir = client
    file_path = upload_dir / "example.txt"
    file_path.write_text("ok", encoding="utf-8")

    response = test_client.get("/download/example.txt")

    assert response.status_code == 200
    assert response.content == b"ok"


def test_download_file_rejects_parent_dir_traversal(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(server, "UPLOAD_DIR_PATH", upload_dir.resolve())

    with pytest.raises(HTTPException) as exc:
        server.build_safe_upload_path("../secret.txt")

    assert exc.value.status_code == 400


def test_download_file_rejects_encoded_parent_dir_traversal(client):
    test_client, _ = client

    response = test_client.get("/download/%2e%2e%2Fsecret.txt")

    assert response.status_code == 400
    assert response.json()["detail"] == "Nome de arquivo inválido"


def test_download_file_rejects_absolute_path(client):
    test_client, _ = client

    response = test_client.get("/download/%2Fetc%2Fpasswd")

    assert response.status_code == 400
    assert response.json()["detail"] == "Nome de arquivo inválido"


def test_download_file_not_found_returns_404(client):
    test_client, _ = client

    response = test_client.get("/download/missing.txt")

    assert response.status_code == 404
    assert response.json()["detail"] == "Arquivo não encontrado"


def test_build_safe_upload_path_rejects_traversal(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(server, "UPLOAD_DIR_PATH", upload_dir.resolve())

    with pytest.raises(HTTPException) as exc:
        server.build_safe_upload_path("../secret.txt")

    assert exc.value.status_code == 400


def test_build_safe_upload_path_rejects_absolute(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(server, "UPLOAD_DIR_PATH", upload_dir.resolve())

    with pytest.raises(HTTPException) as exc:
        server.build_safe_upload_path("/etc/passwd")

    assert exc.value.status_code == 400


def test_build_safe_upload_path_valid(monkeypatch, tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(server, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(server, "UPLOAD_DIR_PATH", upload_dir.resolve())

    safe_name, resolved_path = server.build_safe_upload_path("folder/file.txt")

    assert safe_name == str(Path("folder/file.txt"))
    assert resolved_path == (upload_dir / "folder" / "file.txt").resolve()
