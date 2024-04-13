import logging

import grpc
from grpc_reflection.v1alpha import reflection
from proto import user_pb2, user_pb2_grpc
from src.database import DatabaseManager 

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        logging.info("User Service successfully initialized!")

    # TODO: methods from proto


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

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting user server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()