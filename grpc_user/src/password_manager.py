import hashlib


class Hasher:
    @staticmethod
    def hash_md5(password: str) -> str:
        """
        Хэширует пароль в md5
        """
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode("utf-8"))
        return md5_hash.hexdigest()

    @staticmethod
    def hash_sha256(password: str) -> str:
        """
        Хэширует пароль в sha256
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode("utf-8"))
        return sha256_hash.hexdigest()
