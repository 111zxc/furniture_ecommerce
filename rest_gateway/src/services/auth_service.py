import grpc

from rest_gateway.proto import authorization_pb2, authorization_pb2_grpc
from rest_gateway.src.config import config

"""
This module contains authentication service related functions.

The `issue_token` function sends an `IssueTokenRequest` to the `Authorization` service
and returns the issued token.

The `get_user_id` function sends a `GetUserInfoFromTokenRequest` to the `Authorization`
service and returns the user ID by his token.
"""

AUTH_SERVICE_ADDRESS = f"{config.AUTH_SERVICE_HOSTNAME}:{config.AUTH_SERVICE_PORT}"


def issue_token(user_id: int) -> str:
    """
    Issues a token for a given user ID.

    Args:
        user_id (int): The ID of the user for whom to issue a token.

    Returns:
        str: The issued token.
    """
    with grpc.insecure_channel(AUTH_SERVICE_ADDRESS) as channel:
        client = authorization_pb2_grpc.AuthorizationStub(channel)
        request = authorization_pb2.IssueTokenRequest(user_id=int(user_id))
        response = client.IssueToken(request)
    return response.token


def get_user_id(token: str) -> int:
    """
    Retrieves a user's ID based on their authentication token.

    Args:
        token (str): The authentication token of the user.

    Returns:
        int: The ID of the user associated with the token, or -1 if the token is invalid.
    """
    with grpc.insecure_channel(AUTH_SERVICE_ADDRESS) as channel:
        try:
            client = authorization_pb2_grpc.AuthorizationStub(channel)
            request = authorization_pb2.GetUserInfoFromTokenRequest(token=token)
            response = client.GetUserInfoFromToken(request)
        except grpc._channel._InactiveRpcError as e:
            return -1
    return response.user_id
