import logging

import grpc
from grpc_reflection.v1alpha import reflection
from proto import user_pb2, user_pb2_grpc
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.models import Password, User
from src.password_service import Hasher
from src.postgre_service import DatabaseManager


class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        logging.info("User Service successfully initialized!")

    async def CreateUser(self, request, context):
        async with self.db_manager.get_session() as session:
            new_user = User(username=request.username, email=request.email)
            new_password = Password(
                md5_password=Hasher.hash_md5(request.password),
                sha256_password=Hasher.hash_sha256(request.password),
            )
            new_user.password = new_password
            session.add(new_user)

            await session.commit()
            await session.refresh(new_user)
        return user_pb2.CreateUserResponse(user_id=str(new_user.id))

    async def GetUser(self, request, context):
        async with self.db_manager.get_session() as session:
            user = await session.execute(
                select(User).where(User.id == int(request.user_id))
            )
            user = user.scalars().first()

            if user is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.GetUserResponse()

            response = user_pb2.GetUserResponse(
                user=user_pb2.User(
                    id=str(user.id),
                    username=user.username,
                    email=user.email,
                    role=user.role,
                )
            )
        return response

    async def UpdateUser(self, request, context):
        async with self.db_manager.get_session() as session:
            user = await session.execute(
                select(User).where(User.id == int(request.user_id))
            )
            user = user.scalars().first()

            if user is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.UpdateUserResponse(success=False)

            if request.updated_user.username:
                user.username = request.updated_user.username
            if request.updated_user.email:
                user.email = request.updated_user.email
            if request.updated_user.role:
                user.role = request.updated_user.role

            await session.commit()
            await session.refresh(user)

        return user_pb2.UpdateUserResponse(success=True)

    async def DeleteUser(self, request, context):
        async with self.db_manager.get_session() as session:
            user = await session.execute(
                select(User).where(User.id == int(request.user_id))
            )
            user = user.scalars().first()

            if user is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.DeleteUserResponse(success=False)

            user.deleted = True
            await session.commit()

        return user_pb2.DeleteUserResponse(success=True)

    async def CheckCredentials(self, request, context):
        async with self.db_manager.get_session() as session:
            user = await session.execute(
                select(User)
                .options(joinedload(User.password))
                .where(User.username == request.username)
            )
            user = user.scalars().first()

            if user is None:
                return user_pb2.CheckCredentialsResponse(user_id="-1")

            if user.password.md5_password == Hasher.hash_md5(
                request.password
            ) or user.password.sha256_password == Hasher.hash_sha256(request.password):
                return user_pb2.CheckCredentialsResponse(user_id=str(user.id))
            else:
                return user_pb2.CheckCredentialsResponse(user_id="-1")


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
