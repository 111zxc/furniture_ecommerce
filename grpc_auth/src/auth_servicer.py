import logging

import grpc

from grpc_auth.proto import authorization_pb2, authorization_pb2_grpc
from grpc_auth.src.jwt_manager import JwtManager
from grpc_auth.src.redis_manager import RedisManager


class AuthorizationServicer(authorization_pb2_grpc.AuthorizationServicer):
    def __init__(self) -> None:
        self.auth_manager = JwtManager()
        self.redis_manager = RedisManager()
        logging.info("Authorization Service successfully initialized!")

    async def IssueToken(self, request, context):
        token = self.auth_manager.generate_token(request.user_id)
        logging.info("Issued token %s for user %s", token, request.user_id)
        return authorization_pb2.IssueTokenResponse(token=token)

    async def VerifyToken(self, request, context):
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

    async def RevokeToken(self, request, context):
        await self.redis_manager.add_revoked_token(request.token)
        logging.info("token %s is revoked", request.token)
        return authorization_pb2.RevokeTokenResponse(success=True)

    async def GetUserInfoFromToken(self, request, context):
        revoked = await self.redis_manager.is_token_revoked(request.token)
        if revoked:
            logging.error("Token %s has been revoked", request.token)
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Token has been revoked")
            return authorization_pb2.GetUserInfoFromTokenResponse(user_id=-1)

        user_id = self.auth_manager.get_user_info_from_token(request.token)
        logging.info("got info for user %d with token %s", user_id, request.token)
        return authorization_pb2.GetUserInfoFromTokenResponse(user_id=user_id)
