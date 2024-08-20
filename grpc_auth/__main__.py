import asyncio
import logging

from grpc_auth.src.server import serve as serve_authorization_service


async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        authorization_service_task = asyncio.create_task(serve_authorization_service())
        await asyncio.gather(authorization_service_task)
    except Exception as e:
        logging.error("Service encountered an error: {}".format(e))


if __name__ == "__main__":
    asyncio.run(main())
