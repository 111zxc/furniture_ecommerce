import asyncio
import logging


from grpc_product.src.server import serve as server_product_service


async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        product_service_task = asyncio.create_task(server_product_service())
        await asyncio.gather(product_service_task)
    except Exception as e:
        logging.error("Service encountered an error: {}".format(e))
        raise


if __name__ == "__main__":
    asyncio.run(main())
