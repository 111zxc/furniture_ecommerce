import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the application.

    This class contains configuration settings from environment variables.
    """

    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME")
    POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    SERVER_PORT: str = os.getenv("SERVER_PORT")


config = Config()
