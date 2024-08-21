import logging

import grpc

from grpc_auth.proto import authorization_pb2, authorization_pb2_grpc
from grpc_auth.src.jwt_manager import JwtManager
from grpc_auth.src.redis_manager import RedisManager


class AuthorizationServicer(authorization_pb2_grpc.AuthorizationServicer):
    """
    A service for handling authorization-related tasks.

    This service provides methods for issuing, verifying, and revoking tokens.
    It also handles retrieving user information from tokens.

    Attributes:
        auth_manager (JwtManager): The manager for handling JWT-related tasks.
        redis_manager (RedisManager): The manager for handling Redis-related tasks.

    Methods:
        IssueToken: Issues a token for a given user ID.
        VerifyToken: Verifies a given token by checking its revocation status and validity.
        RevokeToken: Revokes a given token by adding it to the list of revoked tokens.
        GetUserInfoFromToken: Retrieves user information from a given token.
    """

    def __init__(self) -> None:
        self.auth_manager = JwtManager()
        self.redis_manager = RedisManager()
        logging.info("Authorization Service successfully initialized!")

    async def IssueToken(
        self,
        request: authorization_pb2.IssueTokenRequest,
        context: grpc.aio.ServicerContext,
    ) -> authorization_pb2.IssueTokenResponse:
        """
        Issues a token for a given user ID.

        Args:
            request: The request object containing the user ID.
            context: The context object for the gRPC call.

        Returns:
            authorization_pb2.IssueTokenResponse: A response object containing the issued token.
        """
        token = self.auth_manager.generate_token(request.user_id)
        logging.info("Issued token %s for user %s", token, request.user_id)
        return authorization_pb2.IssueTokenResponse(token=token)

    async def VerifyToken(
        self,
        request: authorization_pb2.VerifyTokenRequest,
        context: grpc.aio.ServicerContext,
    ) -> authorization_pb2.VerifyTokenResponse:
        """
        Verifies a given token by checking its revocation status and validity.

        Args:
            request: The request object containing the token to be verified.
            context: The context object for the gRPC call.

        Returns:
            authorization_pb2.VerifyTokenResponse: A response object containing the verification result.
        """
        revoked = await self.redis_manager.is_token_revoked(request.token)
        if revoked:
            logging.info("Token %s was verified revoked", request.token)
            return authorization_pb2.VerifyTokenResponse(valid=False)

        valid = self.auth_manager.verify_token(request.token)
        msg = "Token {} was verified {}".format(
            request.token, "valid" if valid else "expired"
        )
        logging.info(msg)
        return authorization_pb2.VerifyTokenResponse(valid=valid)

    async def RevokeToken(
        self,
        request: authorization_pb2.RevokeTokenRequest,
        context: grpc.aio.ServicerContext,
    ) -> authorization_pb2.RevokeTokenResponse:
        """
        Revokes a given token by adding it to the list of revoked tokens.

        Args:
            request: The request object containing the token to be revoked.
            context: The context object for the gRPC call.

        Returns:
            authorization_pb2.RevokeTokenResponse: A response object containing the revocation result.
        """
        await self.redis_manager.add_revoked_token(request.token)
        logging.info("token %s is revoked", request.token)
        return authorization_pb2.RevokeTokenResponse(success=True)

    async def GetUserInfoFromToken(
        self,
        request: authorization_pb2.GetUserInfoFromTokenRequest,
        context: grpc.aio.ServicerContext,
    ) -> authorization_pb2.GetUserInfoFromTokenResponse:
        """
        Retrieves user information from a given token.

        Args:
            request: The request object containing the token.
            context: The context object for the gRPC call.

        Returns:
            authorization_pb2.GetUserInfoFromTokenResponse: A response object containing the user ID.
        """
        revoked = await self.redis_manager.is_token_revoked(request.token)
        if revoked:
            logging.error("Token %s has been revoked", request.token)
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Token has been revoked")
            return authorization_pb2.GetUserInfoFromTokenResponse(user_id=-1)

        user_id = self.auth_manager.get_user_info_from_token(request.token)
        logging.info("got info for user %d with token %s", user_id, request.token)
        return authorization_pb2.GetUserInfoFromTokenResponse(user_id=user_id)
