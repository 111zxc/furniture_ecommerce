import asyncio
import logging

from dotenv import load_dotenv
from src.user_controller import serve as server_user_service


async def main():
    logging.basicConfig(level=logging.INFO)

    user_service_task = asyncio.create_task(server_user_service())

    await asyncio.gather(user_service_task)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
