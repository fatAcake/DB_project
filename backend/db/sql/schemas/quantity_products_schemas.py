from pydantic import BaseModel

class QuantityProductBase(BaseModel):
    count: int
    product_id: int

class QuantityProductCreate(QuantityProductBase):
    pass

class QuantityProductUpdate(BaseModel):
    count: int

class QuantityProductInfo(QuantityProductBase):
    id: int