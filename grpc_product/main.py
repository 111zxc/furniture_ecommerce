import asyncio
import logging

from dotenv import load_dotenv

from src.product_controller import serve as server_product_service


async def main():
    logging.basicConfig(level=logging.INFO)

    product_service_task = asyncio.create_task(server_product_service())

    await asyncio.gather(product_service_task)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
