import logging

import grpc
from google.protobuf.json_format import MessageToDict
from grpc_reflection.v1alpha import reflection

from proto import product_pb2, product_pb2_grpc
from src.mongo_service import ProductDB


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self) -> None:
        self.db = ProductDB("my_database", "products")
        logging.info("Product Service successfully initialized!")

    def CreateProduct(self, request, context):
        product_fields = {
            "name": request.product.name,
            "description": request.product.description,
            "price": request.product.price,
            "state": request.product.state,
            "owner_id": request.product.owner_id,
        }
        product_id = self.db.create_product(product_fields)
        # Создаем объект Product с использованием извлеченных полей
        return product_pb2.Product(
            _id=product_id,
            name=product_fields["name"],
            description=product_fields["description"],
            price=product_fields["price"],
            state=product_fields["state"],
            owner_id=product_fields["owner_id"],
        )

    def GetProduct(self, request, context):
        product = self.db.get_product(request.id)
        if product is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.Product()
        return product_pb2.Product(
            _id=str(product["_id"]),
            name=product["name"],
            description=product["description"],
            price=product["price"],
            state=product["state"],
            owner_id=product["owner_id"],
        )

    def UpdateProduct(self, request, context):
        product_dict = MessageToDict(request.product)
        success = self.db.update_product(request.product._id, product_dict)
        if not success:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.Product()
        return request.product

    def DeleteProduct(self, request, context):
        success = self.db.delete_product(request.id)
        if not success:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.DeleteProductResponse(success=False)
        return product_pb2.DeleteProductResponse(success=True)


async def serve():
    server = grpc.aio.server()
    product_servicer = ProductServicer()

    product_pb2_grpc.add_ProductServiceServicer_to_server(product_servicer, server)

    SERVICE_NAMES = (
        product_pb2.DESCRIPTOR.services_by_name["ProductService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = "[::]:50053"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting product server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()
