from pydantic import BaseModel, Field


class Item(BaseModel):
    phone: str = Field(..., json_schema_extra={"example": "89090000000"}, pattern=r'^\d{11}$')
    address: str = Field(..., json_schema_extra={"example": "123 Main St, Lazytown, Country"})
