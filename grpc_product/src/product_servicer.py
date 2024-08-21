import logging

import grpc
from google.protobuf.json_format import MessageToDict

from grpc_product.proto import product_pb2, product_pb2_grpc
from grpc_product.src.models import Product
from grpc_product.src.mongo_manager import ProductDB


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    """
    A service for handling product-related tasks.

    This service provides methods for creating, retrieving, updating, and deleting products.

    Attributes:
        db (ProductDB): The manager for handling MongoDB-related tasks.

    Methods:
        CreateProduct: Creates a product in the database.
        GetProduct: Retrieves a product from the database.
        UpdateProduct: Updates a product in the database.
        DeleteProduct: Deletes a product from the database.
    """

    def _handle_error(self, context: grpc.ServicerContext, error: Exception) -> None:
        """
        Handles an error by logging it and setting the gRPC service context.

        Args:
            context (grpc.ServicerContext): The gRPC service context.
            error (Exception): The error to be handled.
        """
        logging.error("Failed to perform operation: {}".format(error))
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Failed to perform operation")

    def __init__(self) -> None:
        self.db = ProductDB()
        logging.info("Product Service successfully initialized!")

    def CreateProduct(
        self, request: product_pb2.Product, context: grpc.ServicerContext
    ) -> product_pb2.Product:
        """
        Creates a new product in the database.

        Args:
            request (product_pb2.Product): The product to be created.
            context (grpc.ServicerContext): The gRPC service context.

        Returns:
            product_pb2.Product: The created product.
        """
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
            self._handle_error(context, e)
            return product_pb2.Product()

    def GetProduct(
        self, request: product_pb2.GetProductRequest, context: grpc.ServicerContext
    ) -> product_pb2.Product:
        """
        Retrieves a product from the database based on the provided product ID.

        Args:
            request (product_pb2.GetProductRequest): The request containing the product ID.
            context (grpc.ServicerContext): The gRPC service context.

        Returns:
            product_pb2.Product: The retrieved product if found, otherwise an empty product.
        """
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
            self._handle_error(context, e)
            return product_pb2.Product()

    def UpdateProduct(
        self, request: product_pb2.Product, context: grpc.ServicerContext
    ) -> product_pb2.Product:
        """
        Updates a product in the database based on the provided product information.

        Args:
            request (product_pb2.Product): The request containing the product information to be updated.
            context (grpc.ServicerContext): The gRPC service context.

        Returns:
            product_pb2.Product: The updated product if successful, otherwise an empty product.
        """
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
            self._handle_error(context, e)
            return product_pb2.Product()

    def DeleteProduct(
        self, request: product_pb2.GetProductRequest, context: grpc.ServicerContext
    ) -> product_pb2.DeleteProductResponse:
        """
        Deletes a product from the database based on the provided product ID.

        Args:
            request (product_pb2.GetProductRequest): The request containing the product ID.
            context (grpc.ServicerContext): The gRPC service context.

        Returns:
            product_pb2.DeleteProductResponse: The response indicating whether the product was deleted successfully.
        """
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
            self._handle_error(context, e)
            return product_pb2.DeleteProductResponse(success=False)
