import logging

import grpc
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from grpc_user.proto import user_pb2, user_pb2_grpc
from grpc_user.src.models import Password, User
from grpc_user.src.password_service import Hasher
from grpc_user.src.postgre_service import DatabaseManager


class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        logging.info("User Service successfully initialized!")

    async def CreateUser(self, request, context):
        try:
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
                logging.info("User {} successfully created!".format(new_user.id))
            return user_pb2.CreateUserResponse(user_id=str(new_user.id))
        except Exception as e:
            logging.error("Error creating user: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.CreateUserResponse()
        
    async def GetUser(self, request, context):
        try:
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
            logging.info("User {} successfully received!".format(request.user_id))
            return response
        except Exception as e:
            logging.error("Error getting user: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.GetUserResponse()

    async def UpdateUser(self, request, context):
        try:
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

            logging.info("User {} successfully updated!".format(request.user_id))
            return user_pb2.UpdateUserResponse(success=True)
        except Exception as e:
            logging.error("Error updating user: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UpdateUserResponse(success=False)

    async def DeleteUser(self, request, context):
        try:
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
            logging.info("User {} successfully deleted!".format(request.user_id))
            return user_pb2.DeleteUserResponse(success=True)
        except Exception as e:
            logging.error("Error deleting user: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.DeleteUserResponse(success=False)

    async def CheckCredentials(self, request, context):
        try:
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
        except Exception as e:
            logging.error("Error checking credentials: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.CheckCredentialsResponse(user_id="-1")