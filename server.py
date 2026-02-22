import uvicorn

from chatapp.config.settings import settings
from chatapp.infrastructure.http.file_server import app

if __name__ == "__main__":
    uvicorn.run(app, host=settings.file_server_host, port=settings.file_server_port)
