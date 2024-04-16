from pydantic import BaseModel


class LoginData(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    password: str
    email: str


class FullUser(BaseModel):
    username: str
    email: str
    role: str


class Product(BaseModel):
    name: str
    description: str
    price: float
    state: str
    owner_id: str
