import logging
from typing import Any, Literal

from redis import asyncio as aioredis

from grpc_auth.src.config import config


class RedisManager:
    def __init__(self) -> None:
        self.redis_pool = None

    async def connect(self) -> None:
        """
        Establishes a connection to the Redis database.

        This method sets up a connection pool to the Redis database using the hostname specified in the config.
        """
        try:
            host = config.REDIS_HOSTNAME
            self.redis_pool = aioredis.ConnectionPool.from_url(f"redis://{host}")
            logging.info("Connected to Redis")
        except Exception as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise

    async def close(self) -> None:
        """
        Closes the connection to the Redis database.

        This method checks if a connection pool exists and if so, closes it asynchronously.
        """
        if self.redis_pool:
            await self.redis_pool.aclose()
            logging.info("Disconnected from Redis")

    async def add_revoked_token(self, token: str) -> None:
        """
        Adds a revoked token to the Redis database.

        Args:
            token (str): The token to be added to the revoked tokens set.
        """
        async with aioredis.Redis.from_pool(self.redis_pool) as conn:
            await conn.sadd("revoked_tokens", token)

    async def is_token_revoked(self, token: str) -> bool:
        """
        Checks if a given token is revoked by querying the Redis database.

        Args:
            token (str): The token to be checked for revocation.

        Returns:
            bool: True if the token is revoked, False otherwise.
        """
        async with aioredis.Redis.from_pool(self.redis_pool) as conn:
            result = await conn.sismember("revoked_tokens", token)
        return result
