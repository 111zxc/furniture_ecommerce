import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the application.

    This class contains configuration settings from environment variables.
    """

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
    SERVER_PORT = os.getenv("SERVER_PORT", "50053")


config = Config()
