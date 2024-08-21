import logging
from datetime import datetime, timedelta

import jwt

from grpc_auth.src.config import config


class JwtManager:
    """
    Manager for handling JWT-related tasks.

    This class provides methods for generating and verifying JWT tokens.
    It also handles token revocation.

    Attributes:
        secret_key (str): The secret key used to sign and verify JWT tokens.

    Methods:
        generate_token: Generates a JWT token for a given user ID.
        verify_token: Verifies a given JWT token.
    """

    JWT_ALGORITHM = ["HS256"]

    def __init__(self) -> None:
        self.secret_key = config.JWT_SECRET_KEY

    def generate_token(self, user_id: int) -> str:
        """
        Generates a JWT token for a given user ID.

        Args:
            user_id (int): The ID of the user to generate the token for.

        Returns:
            str: A JWT token that can be used for authentication.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.now() + timedelta(days=1),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.JWT_ALGORITHM[0])
        return token

    def verify_token(self, token: str) -> bool:
        """
        Verifies a given JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            jwt.decode(token, self.secret_key, algorithms=self.JWT_ALGORITHM)
            return True
        except jwt.ExpiredSignatureError:
            logging.error("JWT token has expired")
            return False
        except jwt.InvalidTokenError:
            logging.error("Invalid JWT token")
            return False

    def get_user_info_from_token(self, token: str) -> int | None:
        """
        Retrieves user information from a given JWT token.

        Args:
            token (str): The JWT token to extract user information from.

        Returns:
            int or None: The user ID if the token is valid, None if the token has expired, or -1 if the token is invalid.
        """
        try:
            decoded_token = jwt.decode(token, self.secret_key, self.JWT_ALGORITHM)
            return decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            logging.error("JWT token has expired")
            return None
        except jwt.InvalidTokenError:
            logging.error("Invalid JWT token")
            return None
