import logging

import grpc
from grpc_reflection.v1alpha import reflection
from proto import authorization_pb2, authorization_pb2_grpc
from src.auth_service import AuthManager
from src.redis_service import RedisManager


class AuthorizationServicer(authorization_pb2_grpc.AuthorizationServicer):
    def __init__(self) -> None:
        self.auth_manager = AuthManager()
        self.redis_manager = RedisManager()
        logging.info("Authorization Service successfully initialized!")

    async def IssueToken(self, request, context):
        token = self.auth_manager.generate_token(request.user_id)
        logging.info(f"Issued token {token} for user {request.user_id}")
        return authorization_pb2.IssueTokenResponse(token=token)

    async def VerifyToken(self, request, context):
        revoked = await self.redis_manager.is_token_revoked(request.token)
        if revoked:
            logging.info(f"Token {request.token} was verified revoked")
            return authorization_pb2.VerifyTokenResponse(valid=False)

        valid = self.auth_manager.verify_token(request.token)
        logging.info(
            f"Token {request.token} was\
                    verified {'valid' if valid else 'expired'}"
        )
        return authorization_pb2.VerifyTokenResponse(valid=valid)

    async def RevokeToken(self, request, context):
        await self.redis_manager.add_revoked_token(request.token)
        logging.info(f"token {request.token} is revoked")
        return authorization_pb2.RevokeTokenResponse(success=True)

    async def GetUserInfoFromToken(self, request, context):
        revoked = await self.redis_manager.is_token_revoked(request.token)
        if revoked:
            logging.error("Token has been revoked")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Token has been revoked")
            return authorization_pb2.GetUserInfoFromTokenResponse(user_id=-1)

        user_id = self.auth_manager.get_user_info_from_token(request.token)
        logging.info(f"got info for user {user_id} by token {request.token}")
        return authorization_pb2.GetUserInfoFromTokenResponse(user_id=user_id)


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
