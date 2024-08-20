import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_HOSTNAME = os.getenv("MONGO_HOSTNAME", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "my_database")
    MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "products")
    SERVER_PORT = os.getenv("SERVER_PORT", "50053")

config = Config()
