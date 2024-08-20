import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")


config = Config()
