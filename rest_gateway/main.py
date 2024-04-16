from fastapi import FastAPI, Header
from src.auth_service import check_rights
from src.models import FullUser, LoginData, Product, User
from src.product_service import (create_product, delete_product, get_product,
                                 update_product)
from src.user_service import (check_credentials, create_user, delete_user,
                              get_user, update_user)

app = FastAPI()


@app.post("/api/v1/users/create")
async def create_user_endpoint(user: User):
    created_user = create_user(user)
    return created_user


@app.get("/api/v1/users/{user_id}")
async def get_user_endpoint(user_id: str):
    got_user = get_user(user_id)
    return got_user


@app.put("/api/v1/users/{user_id}")
async def update_user_endpoint(user_id: str, user: FullUser, token: str = Header(None)):
    token_user_id = check_rights(token)
    if token_user_id == -1 or token_user_id != int(user_id):
        return {"error": "wrong token"}
    result = update_user(user_id, user)
    return result


@app.delete("/api/v1/users/{user_id}")
async def delete_user_endpoint(user_id: str, token: str = Header(None)):
    token_user_id = check_rights(token)
    if token_user_id == -1 or token_user_id != int(user_id):
        return {"error": "wrong token"}
    result = delete_user(user_id)
    return result


@app.post("/api/v1/products/")
async def create_product_endpoint(product: Product, token: str = Header(None)):
    token_user_id = check_rights(token)
    if token_user_id == -1 or token_user_id != int(product.owner_id):
        return {"error": "wrong token"}
    result = create_product(product)
    return result


@app.get("/api/v1/products/{product_id}")
async def get_product_endpoint(product_id: str):
    result = get_product(product_id)
    return result


@app.put("/api/v1/products/{product_id}")
async def update_product_endpoint(product_id: str, product: Product):
    # TODO: authorize
    result = update_product(product_id, product)
    return result


@app.delete("/api/v1/products/{product_id}")
async def delete_product_endpoint(product_id: str):
    # TODO: authorize
    result = delete_product(product_id)
    return result


@app.post("/api/v1/users/login")
async def login_user(login_data: LoginData):
    result = check_credentials(login_data)
    return result
