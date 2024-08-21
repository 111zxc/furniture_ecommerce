import pytest
from grpc_auth.src.jwt_manager import JwtManager

def test_verify_token():
    jwt_manager = JwtManager()
    token = jwt_manager.generate_token(1)
    assert jwt_manager.verify_token(token) is True

def test_verify_token_expired():
    jwt_manager = JwtManager()
    token = jwt_manager.generate_token(1)
    token = token[:-1] + '0'
    assert jwt_manager.verify_token(token) is False

def test_verify_token_invalid():
    jwt_manager = JwtManager()
    token = 'invalid_token'
    assert jwt_manager.verify_token(token) is False