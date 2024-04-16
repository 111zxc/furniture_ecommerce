import logging
import os
from datetime import datetime, timedelta

import jwt


class AuthManager:
    JWT_ALGORITHM = ["HS256"]

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")

    def generate_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow()
            + timedelta(days=1),  # Установка срока действия токена на 1 день
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.JWT_ALGORITHM[0])
        return token

    def verify_token(self, token):
        try:
            jwt.decode(token, self.secret_key, algorithms=self.JWT_ALGORITHM)
            return True
        except jwt.ExpiredSignatureError:
            logging.error("JWT token has expired")
            return False
        except jwt.InvalidTokenError:
            logging.error("Invalid JWT token")
            return False

    def get_user_info_from_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.secret_key, self.JWT_ALGORITHM)
            return decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            logging.error("JWT token has expired")
            return None
        except jwt.InvalidTokenError:
            logging.error("Invalid JWT token")
            return -1