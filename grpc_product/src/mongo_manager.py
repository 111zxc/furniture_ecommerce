from bson.objectid import ObjectId
from pymongo import MongoClient
import logging

from grpc_product.src.config import config


class ProductDB:
    def __init__(self):
        DSN = f"mongodb://{config.MONGO_HOSTNAME}:{config.MONGO_PORT}"
        self.client = MongoClient(DSN)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_COLLECTION_NAME]

    def create_product(self, product):
        try:
            result = self.collection.insert_one(product)
            return str(result.inserted_id)
        except Exception as e:
            logging.error("Failed to create product: {}".format(e))
            raise

    def get_product(self, product_id):
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            return product
        except Exception as e:
            logging.error("Failed to get product: {}".format(e))
            raise

    def update_product(self, product_id, product):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(product_id)}, {"$set": product}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Failed to update product: {}".format(e))
            raise

    def delete_product(self, product_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Failed to delete product: {}".format(e))
            raise

    def get_all_products(self):
        try:
            products = self.collection.find()
            return list(products)
        except Exception as e:
            logging.error("Failed to get all products: {}".format(e))
            raise