import asyncio
import logging

from grpc_user.src.server import serve as server_user_service


async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        user_service_task = asyncio.create_task(server_user_service())
        await asyncio.gather(user_service_task)
    except Exception as e:
        logging.error("Service encountered an error: {}".format(e))
        raise

if __name__ == "__main__":
    asyncio.run(main())
