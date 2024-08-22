import grpc

from rest_gateway.proto import user_pb2, user_pb2_grpc
from rest_gateway.src.config import config
from rest_gateway.src.services.auth_service import issue_token

USER_SERVICE_ADDRESS = f"{config.USER_SERVICE_HOSTNAME}:{config.USER_SERVICE_PORT}"


def create_user(user: user_pb2.User) -> dict[str, str]:
    """
    Creates a new user and returns the created user's details.

    Args:
        user (user_pb2.User): The user to be created.

    Returns:
        dict[str, str]: A dictionary containing the created user's id, username, and email.
    """
    with grpc.insecure_channel(USER_SERVICE_ADDRESS) as channel:
        client = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.CreateUserRequest(
            username=user.username, password=user.password, email=user.email
        )
        response = client.CreateUser(request)

    created_user = {
        "id": response.user_id,
        "username": user.username,
        "email": user.email,
    }
    return created_user


def get_user(user_id: int) -> dict[str, str]:
    """
    Retrieves a user from the UserService by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: A dictionary containing the user's ID, username, email, and role.
            If the user is not found, returns a dictionary with the key "error"
            and the value "User not found".
    """
    try:
        with grpc.insecure_channel(USER_SERVICE_ADDRESS) as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.GetUserRequest(user_id=user_id)
            response = client.GetUser(request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    got_user = {
        "id": response.user.id,
        "username": response.user.username,
        "email": response.user.email,
        "role": response.user.role,
    }
    return got_user


def update_user(user_id: int, user: user_pb2.User) -> dict[str, str]:
    """
    Updates a user in the UserService by their ID.

    Args:
        user_id (str): The ID of the user to update.
        user (object): The user object containing the updated username, email, and role.

    Returns:
        dict: A dictionary containing a success flag indicating whether the update was successful.
            If the user is not found, returns a dictionary with the key "error" and the value "User not found".
    """
    try:
        with grpc.insecure_channel(USER_SERVICE_ADDRESS) as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            updated_user = user_pb2.User(
                username=user.username, email=user.email, role=user.role
            )
            update_request = user_pb2.UpdateUserRequest(
                user_id=user_id, updated_user=updated_user
            )
            response = client.UpdateUser(update_request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    result = {"success": response.success}
    return result


def delete_user(user_id: int) -> dict[str, str]:
    """
    Deletes a user in the UserService by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: A dictionary containing a success flag indicating whether the deletion was successful.
            If the user is not found, returns a dictionary with the key "error" and the value "User not found".
    """
    try:
        with grpc.insecure_channel(USER_SERVICE_ADDRESS) as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.DeleteUserRequest(user_id=user_id)
            response = client.DeleteUser(request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    result = {"success": response.success}
    return result


def check_credentials(LoginData) -> dict[str, str]:
    """
    Check the credentials of a user by sending a request to the UserService.

    Args:
        LoginData (object): An object containing the username and password of the user.

    Returns:
        dict: A dictionary containing the token for the authenticated user.
    """
    with grpc.insecure_channel(USER_SERVICE_ADDRESS) as channel:
        client = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.CheckCredentialsRequest(
            username=LoginData.username, password=LoginData.password
        )
        response = client.CheckCredentials(request)
    user_id = response.user_id
    token = issue_token(user_id)
    return {"token": token}
