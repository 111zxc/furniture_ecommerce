import pytest
from grpc_user.src.password_manager import Hasher

def test_hash_md5():
    password = "test_password"
    assert Hasher.hash_md5(password) == Hasher.hash_md5(password)

def test_hash_sha256():
    password = "test_password"
    assert Hasher.hash_sha256(password) == Hasher.hash_sha256(password)

def test_hash_md5_empty_password():
    password = ""
    assert Hasher.hash_md5(password) == Hasher.hash_md5(password)

def test_hash_sha256_empty_password():
    password = ""
    assert Hasher.hash_sha256(password) == Hasher.hash_sha256(password)

def test_hash_md5_none_password():
    password = None
    with pytest.raises(AttributeError):
        Hasher.hash_md5(password)

def test_hash_sha256_none_password():
    password = None
    with pytest.raises(AttributeError):
        Hasher.hash_sha256(password)