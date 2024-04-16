import grpc
from proto import authorization_pb2_grpc, authorization_pb2

def issue_token(user_id):
    with grpc.insecure_channel('localhost:50052') as channel:
        client = authorization_pb2_grpc.AuthorizationStub(channel)
        request = authorization_pb2.IssueTokenRequest(user_id=int(user_id))
        response = client.IssueToken(request)
    return response.token

def check_rights(token):
    with grpc.insecure_channel('localhost:50052') as channel:
        try:
            client = authorization_pb2_grpc.AuthorizationStub(channel)
            request = authorization_pb2.GetUserInfoFromTokenRequest(token=token)
            response = client.GetUserInfoFromToken(request)
        except grpc._channel._InactiveRpcError as e:
            return -1
    return response.user_id