from bson.objectid import ObjectId
from pymongo import MongoClient


class ProductDB:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_product(self, product):
        result = self.collection.insert_one(product)
        return str(result.inserted_id)

    def get_product(self, product_id):
        product = self.collection.find_one({"_id": ObjectId(product_id)})
        return product

    def update_product(self, product_id, product):
        result = self.collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": product}
        )
        return result.modified_count > 0

    def delete_product(self, product_id):
        result = self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    def get_all_products(self):
        products = self.collection.find()
        return list(products)
