import logging

from bson.objectid import ObjectId
from pymongo import MongoClient

from grpc_product.src.config import config
from grpc_product.src.models import Product


class ProductDB:
    """
    Class responsible for managing operations with MongoDB

    Class contains methods for creating, reading, updating and deleting
    products from MongoDB.
    """

    def __init__(self) -> None:
        DSN = f"mongodb://{config.MONGO_HOSTNAME}:{config.MONGO_PORT}"
        self.client = MongoClient(DSN)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_COLLECTION_NAME]

    def create_product(self, product: Product) -> str:
        """
        Creates a new product in the MongoDB collection.

        Args:
            product (Product): The product object to be created.

        Returns:
            str: The ID of the inserted product.
        """
        try:
            result = self.collection.insert_one(product)
            return str(result.inserted_id)
        except Exception as e:
            logging.error("Failed to create product: {}".format(e))
            raise

    def get_product(self, product_id: int) -> Product:
        """
        Retrieves a product from the MongoDB collection by its ID.

        Args:
            product_id (str): The ID of the product to be retrieved.

        Returns:
            Product: The product object if found, otherwise raises an exception.
        """
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            return product
        except Exception as e:
            logging.error("Failed to get product: {}".format(e))
            raise

    def update_product(self, product_id: int, product: Product) -> bool:
        """
        Updates a product in the MongoDB collection.

        Args:
            product_id (str): The ID of the product to be updated.
            product (dict): The updated product data.

        Returns:
            bool: True if the product was updated, False otherwise.
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(product_id)}, {"$set": product}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Failed to update product: {}".format(e))
            raise

    def delete_product(self, product_id: int) -> bool:
        """
        Deletes a product from the MongoDB collection.

        Args:
            product_id (int): The ID of the product to be deleted.

        Returns:
            bool: True if the product was deleted, False otherwise.
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Failed to delete product: {}".format(e))
            raise

    def get_all_products(self) -> list[Product]:
        """
        Retrieves all products from the MongoDB collection.

        Returns:
            list[Product]: A list of all products in the collection.
        """
        try:
            products = self.collection.find()
            return list(products)
        except Exception as e:
            logging.error("Failed to get all products: {}".format(e))
            raise
