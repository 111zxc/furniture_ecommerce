from fastapi import FastAPI
from src.user_service import create_user, update_user, delete_user, get_user
from src.product_service import create_product, update_product, delete_product, get_product
from src.models import User, FullUser, Product

app = FastAPI()


@app.post("/api/v1/users/create")
async def create_user_endpoint(user: User):
    created_user = create_user(user)
    return created_user

@app.get('/api/v1/users/{user_id}')
async def get_user_endpoint(user_id: str):
    got_user = get_user(user_id)
    return got_user

@app.put('/api/v1/users/{user_id}')
async def update_user_endpoint(user_id: str, user: FullUser):
    result = update_user(user_id, user)
    return result


@app.delete('/api/v1/users/{user_id}')
async def delete_user_endpoint(user_id: str):
    result = delete_user(user_id)
    return result

@app.post('/api/v1/products/')
async def create_product_endpoint(product: Product):
    result = create_product(product)
    return result

@app.get('/api/v1/products/{product_id}')
async def get_product_endpoint(product_id: str):
    result = get_product(product_id)
    return result

@app.put('/api/v1/products/{product_id}')
async def update_product_endpoint(product_id: str, product: Product):
    result = update_product(product_id, product)
    return result

@app.delete('/api/v1/products/{product_id}')
async def delete_product_endpoint(product_id: str):
    result = delete_product(product_id)
    return result