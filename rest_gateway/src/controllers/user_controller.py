from fastapi import APIRouter, Header

from rest_gateway.src.auth_helper import authorize
from rest_gateway.src.models import FullUser, LoginData, User
from rest_gateway.src.services.auth_service import get_user_id
from rest_gateway.src.services.user_service import (
    check_credentials,
    create_user,
    delete_user,
    get_user,
    update_user,
)

"""
This module contains the user controller, which handles all
user-related operations. This includes creating, reading,
updating and deleting user.

The controller uses the `src.services.user_service` module to perform
the actual operations on users.
"""

router = APIRouter()


@router.post("/create")
def create_user_endpoint(user: User):
    created_user = create_user(user)
    return created_user


@router.get("/{user_id}")
def get_user_endpoint(user_id: str):
    got_user = get_user(user_id)
    return got_user


@authorize(["user", "admin"])
@router.put("/{user_id}")
def update_user_endpoint(user_id: str, user: FullUser, token: str = Header(None)):
    result = update_user(user_id, user)
    return result


@authorize(["admin"])
@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str, token: str = Header(None)):
    result = delete_user(user_id)
    return result


@router.post("/login")
def login_user(login_data: LoginData):
    result = check_credentials(login_data)
    return result
