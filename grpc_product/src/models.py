from bson import ObjectId
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    price: float
    owner_id: int

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda x: str(x)}
