import uvicorn

from chatapp.config.settings import settings
from chatapp.infrastructure.fastapi_server import app

if __name__ == "__main__":
    uvicorn.run(app, host=settings.server_host, port=settings.server_port)
