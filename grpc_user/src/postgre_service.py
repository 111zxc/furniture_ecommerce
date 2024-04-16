import logging
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.models import Base


class DatabaseManager:
    def __init__(self):
        username = os.getenv("POSTGRES_USERNAME")
        password = os.getenv("POSTGRES_PASSWORD")
        url = os.getenv("POSTGRES_URL")
        db_name = os.getenv("POSTGRES_DB_NAME")
        DSN_URL = f"postgresql+asyncpg://{username}:{password}@{url}/{db_name}"
        self.url = DSN_URL

    async def connect(self):
        self.engine = create_async_engine(
            url=self.url, echo=True, pool_size=5, max_overflow=10
        )
        self.get_session = async_sessionmaker(self.engine)
        logging.info("Succesfully connected to PGSQL Database!")

    async def shutdown(self):
        await self.engine.dispose()
        logging.info("Connection to PGSQL Database was closed")

    async def initialize_schema(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Successfully innitialized schema!")
