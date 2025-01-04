from pydantic import BaseModel


class ProductInput(BaseModel):
    name: str
    description: str


class ProductOutput(ProductInput):
    id: int
    created_at: str
    updated_at: str