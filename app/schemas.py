from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)
    description: str


class ProductOutput(ProductInput):
    id: int
    created_at: str
    updated_at: str