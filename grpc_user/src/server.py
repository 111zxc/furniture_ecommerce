import logging

import grpc
from grpc_reflection.v1alpha import reflection

from grpc_user.proto import user_pb2, user_pb2_grpc
from grpc_user.src.config import config
from grpc_user.src.user_servicer import UserServicer


async def serve():
    server = grpc.aio.server()
    user_servicer = UserServicer()
    await user_servicer.db_manager.connect()
    await user_servicer.db_manager.initialize_schema()

    user_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)

    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = f"[::]:{config.SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting user server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()
