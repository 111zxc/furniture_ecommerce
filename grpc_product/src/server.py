import logging

import grpc
from grpc_reflection.v1alpha import reflection

from grpc_product.proto import product_pb2, product_pb2_grpc
from grpc_product.src.config import config
from grpc_product.src.product_servicer import ProductServicer


async def serve():
    server = grpc.aio.server()
    product_servicer = ProductServicer()

    product_pb2_grpc.add_ProductServiceServicer_to_server(product_servicer, server)

    SERVICE_NAMES = (
        product_pb2.DESCRIPTOR.services_by_name["ProductService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = f"[::]:{config.SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting product server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()
