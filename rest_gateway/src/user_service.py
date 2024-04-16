import grpc
from proto import user_pb2_grpc, user_pb2

def create_user(user):
    with grpc.insecure_channel("localhost:50051") as channel:
        client = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.CreateUserRequest(
            username=user.username,
            password=user.password,
            email=user.email
        )
        response = client.CreateUser(request)

    created_user = {
        "id": response.user_id,
        "username": user.username,
        "email": user.email
    }
    return created_user

def get_user(user_id):
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.GetUserRequest(
                user_id=user_id
            )
            response = client.GetUser(request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    got_user = {
        "id": response.user.id,
        "username": response.user.username,
        "email": response.user.email,
        "role": response.user.role
    }
    return got_user

def update_user(user_id, user):
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            updated_user = user_pb2.User(
                username=user.username,
                email=user.email,
                role=user.role
            )
            update_request = user_pb2.UpdateUserRequest(
                user_id=user_id,
                updated_user=updated_user
            )
            response = client.UpdateUser(update_request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    result = {
        "success": response.success
    }
    return result

def delete_user(user_id):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            client = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.DeleteUserRequest(user_id=user_id)
            response = client.DeleteUser(request)
    except grpc._channel._InactiveRpcError as e:
        if e.details() == "User not found":
            return {"error": "User not found"}
        raise
    result = {
        "success": response.success
    }
    return result