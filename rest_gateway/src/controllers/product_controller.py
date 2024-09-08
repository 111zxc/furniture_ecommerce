from fastapi import APIRouter, Header

from rest_gateway.src.auth_helper import authorize
from rest_gateway.src.models import Product
from rest_gateway.src.services.auth_service import get_user_id
from rest_gateway.src.services.product_service import (
    create_product,
    delete_product,
    get_product,
    update_product,
    get_all_products,
)

"""
This module contains the product controller, which handles all
product-related operations. This includes creating, reading,
updating and deleting products.

The controller uses the `src.services.product_service` module to perform
the actual operations on the products.
"""

router = APIRouter()


@authorize(["user", "admin"])
@router.post("/")
def create_product_endpoint(product: Product, token: str = Header(None)):
    token_user_id = get_user_id(token)
    if token_user_id == -1 or token_user_id != int(product.owner_id):
        return {"error": "wrong token"}
    result = create_product(product)
    return result


# @authorize(["user", "admin"])
@router.get("/{product_id}")
def get_product_endpoint(product_id: str):
    result = get_product(product_id)
    return result

@router.get('/')
def get_all_products_endpoint():
    result = get_all_products()
    return result


@authorize(["admin"])
@router.put("/{product_id}")
def update_product_endpoint(product_id: str, product: Product):
    result = update_product(product_id, product)
    return result


@authorize(["admin"])
@router.delete("/{product_id}")
def delete_product_endpoint(product_id: str):
    result = delete_product(product_id)
    return result
