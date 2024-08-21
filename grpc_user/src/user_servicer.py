import logging

import grpc
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from grpc_user.proto import user_pb2, user_pb2_grpc
from grpc_user.src.models import Password, User
from grpc_user.src.password_manager import Hasher
from grpc_user.src.postgre_manager import DatabaseManager


class UserServicer(user_pb2_grpc.UserServiceServicer):
    """
    A service for handling user-related tasks.

    This service provides methods for creating, retrieving, updating, and deleting users.

    Attributes:
        db_manager (DatabaseManager): The manager for handling PostgreSQL-related tasks.

    Methods:
        CreateUser: Creates a user in the database.
        GetUser: Retrieves a user from the database.
        UpdateUser: Updates a user in the database.
        DeleteUser: Deletes a user from the database.
        CheckCredentials: Verifies user's credentials.
    """

    def _handle_error(self, context: grpc.ServicerContext, error: Exception) -> None:
        """
        Handles an error by logging it and setting the gRPC service context.

        Args:
            context (grpc.ServicerContext): The gRPC service context.
            error (Exception): The error to be handled.
        """
        logging.error("Failed to perform operation: {}".format(error))
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Failed to perform operation")

    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        logging.info("User Service successfully initialized!")

    async def CreateUser(
        self, request: user_pb2.CreateUserRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.CreateUserResponse:
        """
        Creates a new user in the database.

        Args:
            request (user_pb2.CreateUserRequest): The request containing the user's username, email, and password.
            context (grpc.aio.ServicerContext): The gRPC service context.

        Returns:
            user_pb2.CreateUserResponse: A response containing the ID of the newly created user.
        """
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
            self._handle_error(context, e)
            return user_pb2.CreateUserResponse()

    async def GetUser(
        self, request: user_pb2.GetUserRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.GetUserResponse:
        """
        Retrieves a user from the database based on the provided user ID.

        Args:
            request (user_pb2.GetUserRequest): The request containing the user's ID.
            context (grpc.aio.ServicerContext): The gRPC service context.

        Returns:
            user_pb2.GetUserResponse: A response containing the user's information if found, otherwise an empty response.
        """
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
            self._handle_error(context, e)
            return user_pb2.GetUserResponse()

    async def UpdateUser(
        self, request: user_pb2.UpdateUserRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.UpdateUserResponse:
        """
        Updates a user's information based on the provided request.

        Args:
            request (user_pb2.UpdateUserRequest): The request containing the user's updated information.
            context (grpc.aio.ServicerContext): The gRPC context for the request.

        Returns:
            user_pb2.UpdateUserResponse: A response indicating whether the update was successful.
        """
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
            self._handle_error(context, e)
            return user_pb2.UpdateUserResponse(success=False)

    async def DeleteUser(
        self, request: user_pb2.DeleteUserRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.DeleteUserResponse:
        """
        Deletes a user based on the provided request.

        Args:
            request (user_pb2.DeleteUserRequest): The request containing the user's ID to be deleted.
            context (grpc.aio.ServicerContext): The gRPC context for the request.

        Returns:
            user_pb2.DeleteUserResponse: A response indicating whether the deletion was successful.
        """
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
            self._handle_error(context, e)
            return user_pb2.DeleteUserResponse(success=False)

    async def CheckCredentials(
        self,
        request: user_pb2.CheckCredentialsRequest,
        context: grpc.aio.ServicerContext,
    ) -> user_pb2.CheckCredentialsResponse:
        """
        Checks the provided credentials against the stored user data.

        Args:
            request (user_pb2.CheckCredentialsRequest): The request containing the username and password to be checked.
            context (grpc.aio.ServicerContext): The gRPC context for the request.

        Returns:
            user_pb2.CheckCredentialsResponse: A response containing the user ID if the credentials are valid, otherwise "-1".
        """
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
                ) or user.password.sha256_password == Hasher.hash_sha256(
                    request.password
                ):
                    return user_pb2.CheckCredentialsResponse(user_id=str(user.id))
                else:
                    return user_pb2.CheckCredentialsResponse(user_id="-1")
        except Exception as e:
            self._handle_error(context, e)
            return user_pb2.CheckCredentialsResponse(user_id="-1")
