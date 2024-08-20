import logging
from typing import Any, Literal

from redis import asyncio as aioredis

from grpc_auth.src.config import config


class RedisManager:
    def __init__(self) -> None:
        self.redis_pool = None

    async def connect(self) -> None:
        try:
            host = config.REDIS_HOSTNAME
            self.redis_pool = aioredis.ConnectionPool.from_url(f"redis://{host}")
            logging.info("Connected to Redis")
        except Exception as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise

    async def close(self) -> None:
        if self.redis_pool:
            await self.redis_pool.aclose()
            logging.info("Disconnected from Redis")

    async def add_revoked_token(self, token) -> None:
        async with aioredis.Redis.from_pool(self.redis_pool) as conn:
            await conn.sadd("revoked_tokens", token)

    async def is_token_revoked(self, token) -> Any | Literal[0, 1]:
        async with aioredis.Redis.from_pool(self.redis_pool) as conn:
            result = await conn.sismember("revoked_tokens", token)
        return result
