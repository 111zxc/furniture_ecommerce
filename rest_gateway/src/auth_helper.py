from functools import wraps

from fastapi import Header, HTTPException

from rest_gateway.src.services.auth_service import get_user_id
from rest_gateway.src.services.user_service import get_user


def authorize(roles: list[str]) -> callable:
    """
    A decorator function that authorizes a user based on their role.

    Args:
        roles (list[str]): A list of roles that are allowed to access the decorated function.

    Returns:
        callable: A wrapper function that checks the user's role before calling the original function.
    """

    def wrapper(func: callable) -> callable:
        @wraps(func)
        def wrapped(*args, **kwargs):
            token = kwargs.get("token")
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")

            user_id = get_user_id(token)
            if user_id == -1:
                raise HTTPException(status_code=401, detail="Wrong token")

            user = get_user(user_id)
            if user is None:
                raise HTTPException(status_code=401, detail="User not found")

            if user["role"] not in roles:
                raise HTTPException(status_code=403, detail="Unauthorized")

            return func(*args, **kwargs)

        return wrapped

    return wrapper
