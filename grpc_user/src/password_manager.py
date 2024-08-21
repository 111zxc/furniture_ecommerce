import hashlib


class Hasher:
    """
    Class for hashing passwords.

    This class provides static methods for hashing passwords in different
    formats. The currently supported formats are MD5 and SHA-256.

    """

    @staticmethod
    def hash_md5(password: str) -> str:
        """
        Generates an MD5 hash for a given password.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The MD5 hash of the password.
        """
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode("utf-8"))
        return md5_hash.hexdigest()

    @staticmethod
    def hash_sha256(password: str) -> str:
        """
        Generates a SHA-256 hash for a given password.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The SHA-256 hash of the password.
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode("utf-8"))
        return sha256_hash.hexdigest()
