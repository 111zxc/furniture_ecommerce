import asyncio
import logging

from grpc_auth.src.server import serve


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    try:
        authorization_service_task = asyncio.create_task(serve())
        await asyncio.gather(authorization_service_task)
    except Exception as e:
        logging.error("Service encountered an error: {}".format(e))
        raise

if __name__ == "__main__":
    asyncio.run(main())
