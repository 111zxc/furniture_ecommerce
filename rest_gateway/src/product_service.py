import grpc
from proto import product_pb2, product_pb2_grpc

def create_product(product):
    with grpc.insecure_channel('localhost:50053') as channel:
        client = product_pb2_grpc.ProductServiceStub(channel)
        new_product = product_pb2.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            state=product.state,
            owner_id=product.owner_id
        )
        request = product_pb2.CreateProductRequest(
            product=new_product
        )
        response = client.CreateProduct(request)
    result = {
        "id": response._id
    }
    return result

def get_product(product_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        client = product_pb2_grpc.ProductServiceStub(channel)
        request = product_pb2.GetProductRequest(id=product_id)
        response = client.GetProduct(request)
    result = {
        "id": response._id,
        "name": response.name,
        "description": response.description,
        "price": response.price,
        "state": response.state,
        "owner_id": response.owner_id
    }
    return result

def update_product(product_id, product):
    with grpc.insecure_channel('localhost:50053') as channel:
        client = product_pb2_grpc.ProductServiceStub(channel)
        new_product = product_pb2.Product(
            _id=product_id,
            name=product.name,
            description=product.description,
            price=product.price,
            state=product.state,
            owner_id=product.owner_id
        )
        request = product_pb2.UpdateProductRequest(
            product=new_product
        )
        response = client.UpdateProduct(request)
    result = {
        "id": response._id,
        "name": response.name,
        "description": response.description,
        "price": response.price,
        "state": response.state,
        "owner_id": response.owner_id
    }
    return result

def delete_product(product_id):
    with grpc.insecure_channel('localhost:50053') as channel:
        client = product_pb2_grpc.ProductServiceStub(channel)
        request = product_pb2.DeleteProductRequest(id=product_id)
        response = client.DeleteProduct(request)
    result = {
        "success": response.success
    }
    return result