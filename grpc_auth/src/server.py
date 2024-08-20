import logging

import grpc
from grpc_reflection.v1alpha import reflection

from grpc_auth.proto import authorization_pb2, authorization_pb2_grpc
from grpc_auth.src.auth_servicer import AuthorizationServicer


async def serve():
    server = grpc.aio.server()
    authorization_servicer = AuthorizationServicer()
    await authorization_servicer.redis_manager.connect()

    authorization_pb2_grpc.add_AuthorizationServicer_to_server(
        authorization_servicer, server
    )

    SERVICE_NAMES = (
        authorization_pb2.DESCRIPTOR.services_by_name["Authorization"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting authorization server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()
