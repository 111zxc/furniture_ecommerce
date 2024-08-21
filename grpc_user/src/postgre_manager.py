import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from grpc_user.src.config import config
from grpc_user.src.models import Base


class DatabaseManager:
    """
    Class responsible for managing the connection to the PostgreSQL database.

    Attributes:
        url (str): The URL of the PostgreSQL database.
        engine (sqlalchemy.ext.asyncio.AsyncEngine): The SQLAlchemy engine object.
    """

    def __init__(self) -> None:
        username = config.POSTGRES_USERNAME
        password = config.POSTGRES_PASSWORD
        url = config.POSTGRES_URL
        db_name = config.POSTGRES_DB_NAME
        DSN_URL = f"postgresql+asyncpg://{username}:{password}@{url}/{db_name}"
        self.url = DSN_URL

    async def connect(self) -> None:
        """
        Establishes a connection to the PostgreSQL database using the config URL.

        This method creates an asynchronous engine and session maker, and logs a success message upon completion.
        """
        self.engine = create_async_engine(
            url=self.url, echo=True, pool_size=5, max_overflow=10
        )
        self.get_session = async_sessionmaker(self.engine)
        logging.info("Succesfully connected to PGSQL Database!")

    async def shutdown(self) -> None:
        """
        Shuts down the PostgreSQL database connection.

        This method disposes of the SQLAlchemy engine and logs a success message upon completion.
        """
        await self.engine.dispose()
        logging.info("Connection to PGSQL Database was closed")

    async def initialize_schema(self) -> None:
        """
        Initializes the PostgreSQL database schema by dropping all existing tables and recreating them.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Successfully innitialized schema!")
