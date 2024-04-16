import asyncio
import logging

from dotenv import load_dotenv
from src.auth_controller import serve as serve_authorization_service


async def main():
    logging.basicConfig(level=logging.INFO)

    authorization_service_task = asyncio.create_task(serve_authorization_service())

    await asyncio.gather(authorization_service_task)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())