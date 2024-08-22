import grpc
import grpc._channel

from rest_gateway.proto import product_pb2, product_pb2_grpc
from rest_gateway.src.config import config

PRODUCT_SERVICE_ADDRESS = (
    f"{config.PRODUCT_SERVICE_HOSTNAME}:{config.PRODUCT_SERVICE_PORT}"
)


def create_product(product: product_pb2.Product) -> dict[str, str]:
    """
    Creates a new product using the provided product details.

    Args:
        product: A product object containing name, description, price, state, and owner_id.

    Returns:
        Response (dict["id": str])
    """
    with grpc.insecure_channel(PRODUCT_SERVICE_ADDRESS) as channel:
        client = product_pb2_grpc.ProductServiceStub(channel)
        new_product = product_pb2.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            state=product.state,
            owner_id=product.owner_id,
        )
        request = product_pb2.CreateProductRequest(product=new_product)
        response = client.CreateProduct(request)
    result = {"id": response._id}
    return result


def get_product(product_id: int) -> dict[str, str]:
    """
    Retrieves a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        dict[str, str]: A dictionary containing the product's details, including its ID, name, description, price, state, and owner ID.
        If the product is not found, returns a dictionary with an "error" key and a "Product not found" message.
    """
    try:
        with grpc.insecure_channel(PRODUCT_SERVICE_ADDRESS) as channel:
            client = product_pb2_grpc.ProductServiceStub(channel)
            request = product_pb2.GetProductRequest(id=product_id)
            response = client.GetProduct(request)
    except grpc._channel._InactiveRpcError as e:
        return {"error": "Product not found"}
    result = {
        "id": response._id,
        "name": response.name,
        "description": response.description,
        "price": response.price,
        "state": response.state,
        "owner_id": response.owner_id,
    }
    return result


def update_product(product_id: int, product: product_pb2.Product) -> dict[str, str]:
    """
    Updates a product by its ID.

    Args:
        product_id: The ID of the product to update.
        product: A product object containing the updated product details.

    Returns:
        dict: A dictionary containing the updated product's details, including its ID, name, description, price, state, and owner ID.
        If the product is not found, returns a dictionary with an "error" key and a "Product not found" message.
    """
    try:
        with grpc.insecure_channel(PRODUCT_SERVICE_ADDRESS) as channel:
            client = product_pb2_grpc.ProductServiceStub(channel)
            new_product = product_pb2.Product(
                _id=product_id,
                name=product.name,
                description=product.description,
                price=product.price,
                state=product.state,
                owner_id=product.owner_id,
            )
            request = product_pb2.UpdateProductRequest(product=new_product)
            response = client.UpdateProduct(request)
    except grpc._channel._InactiveRpcError as e:
        return {"error": "Product not found"}
    result = {
        "id": response._id,
        "name": response.name,
        "description": response.description,
        "price": response.price,
        "state": response.state,
        "owner_id": response.owner_id,
    }
    return result


def delete_product(product_id: int) -> dict[str, str]:
    """
    Deletes a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        dict[str, str]: A dictionary containing the result of the deletion operation.
        If the product is not found, returns a dictionary with an "error" key and a "Product not found" message.
    """
    try:
        with grpc.insecure_channel(PRODUCT_SERVICE_ADDRESS) as channel:
            client = product_pb2_grpc.ProductServiceStub(channel)
            request = product_pb2.DeleteProductRequest(id=product_id)
            response = client.DeleteProduct(request)
    except grpc._channel._InactiveRpcError as e:
        return {"error": "Product not found"}
    result = {"success": response.success}
    return result
