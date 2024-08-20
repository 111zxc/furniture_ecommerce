import logging

import grpc
from google.protobuf.json_format import MessageToDict
from grpc_product.proto import product_pb2, product_pb2_grpc

from grpc_product.src.mongo_manager import ProductDB


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self) -> None:
        self.db = ProductDB()
        logging.info("Product Service successfully initialized!")

    def CreateProduct(self, request, context):
        try:
            product_fields = {
                "name": request.product.name,
                "description": request.product.description,
                "price": request.product.price,
                "state": request.product.state,
                "owner_id": request.product.owner_id,
            }
            product_id = self.db.create_product(product_fields)
            logging.info("Product {} successfully created!".format(product_id))

            return product_pb2.Product(
                _id=product_id,
                name=product_fields["name"],
                description=product_fields["description"],
                price=product_fields["price"],
                state=product_fields["state"],
                owner_id=product_fields["owner_id"],
            )
        except Exception as e:
            logging.error("Failed to create product: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create product")
            return product_pb2.Product()

    def GetProduct(self, request, context):
        try:
            product = self.db.get_product(request.id)
            if product is None:
                logging.info("Product {} not found".format(request.id))
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
                return product_pb2.Product()

            logging.info("Product {} found".format(request.id))
            return product_pb2.Product(
                _id=str(product["_id"]),
                name=product["name"],
                description=product["description"],
                price=product["price"],
                state=product["state"],
                owner_id=product["owner_id"],
            )
        except Exception as e:
            logging.error("Failed to get product: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to get product")
            return product_pb2.Product()

    def UpdateProduct(self, request, context):
        try:
            product_dict = MessageToDict(request.product)
            success = self.db.update_product(request.product._id, product_dict)
            if not success:
                logging.info("Product {} not found".format(request.product._id))
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
                return product_pb2.Product()

            logging.info("Product {} successfully updated".format(request.product._id))
            return request.product
        except Exception as e:
            logging.error("Failed to update product: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to update product")
            return product_pb2.Product()

    def DeleteProduct(self, request, context):
        try:
            success = self.db.delete_product(request.id)
            if not success:
                logging.info("Product {} not found".format(request.id))
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
                return product_pb2.DeleteProductResponse(success=False)

            logging.info("Product {} successfully deleted".format(request.id))
            return product_pb2.DeleteProductResponse(success=True)
        except Exception as e:
            logging.error("Failed to delete product: {}".format(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to delete product")
            return product_pb2.DeleteProductResponse(success=False)
