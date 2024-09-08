import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the application.

    This class contains configuration settings from environment variables.
    """

    AUTH_SERVICE_HOSTNAME = os.getenv("AUTH_SERVICE_HOSTNAME", "localhost")
    AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT", "50052")
    USER_SERVICE_HOSTNAME = os.getenv("USER_SERVICE_HOSTNAME", "localhost")
    USER_SERVICE_PORT = os.getenv("USER_SERVICE_PORT", "50051")
    PRODUCT_SERVICE_HOSTNAME = os.getenv("PRODUCT_SERVICE_HOSTNAME", "localhost")
    PRODUCT_SERVICE_PORT = os.getenv("PRODUCT_SERVICE_PORT", "50053")
    HOST= os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", "8080")


config = Config()
print(Config.__dict__)