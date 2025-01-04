from fastapi import FastAPI, Depends, HTTPException, status

from .dao import ProductDao
from.schemas import ProductInput, ProductOutput

from typing import Annotated, List


dao_dependencie = Annotated[ProductDao, Depends(ProductDao)]


app = FastAPI()


@app.get("/api/v1/products/", tags=["Products"])
async def get_all_products(db: dao_dependencie) -> List[ProductOutput]:
    products = await db.get_all_items()
    return [p.to_dict() for p in products]


@app.get("/api/v1/products/{id}/", tags=["Products"])
async def get_all_products(id: int, db: dao_dependencie) -> ProductOutput:
    product = await db.get_one_or_none(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return product.to_dict()


@app.post("/api/v1/products/", tags=["Products"])
async def add_product(
    product: ProductInput,
    db: dao_dependencie
) -> str:
    product_id = await db.add_item(**product.model_dump())
    return f"Product {product_id} was added"


@app.delete("/api/v1/products/{id}", tags=["Products"])
async def delete_product(
    id: int,
    db: dao_dependencie
) -> str:
    product_id = await db.remove_item(id)
    if not product_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return f"Product {product_id} was removed"


@app.put("/api/v1/products/{id}", tags=["Products"])
async def update_product(
    id: int,
    product: ProductInput,
    db: dao_dependencie
) -> str:
    product_id = await db.update_item(id, **product.model_dump())
    if not product_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return f"Product {product_id} was updated"