import uvicorn

from rest_gateway.src.app import app
from rest_gateway.src.config import config

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=int(config.PORT))
