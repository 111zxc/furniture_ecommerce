from fastapi import FastAPI

from rest_gateway.src.controllers import product_controller, user_controller

app = FastAPI()

app.include_router(user_controller.router, prefix="/api/v1/users")
app.include_router(product_controller.router, prefix="/api/v1/products")
