import pytest_asyncio

from app.models import Product
from .database import engine, SessionLocal, db_path

import os


@pytest_asyncio.fixture(scope="session", autouse=True)
async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Product.metadata.create_all)
        yield
        await conn.run_sync(Product.metadata.drop_all)
        await engine.dispose()
        os.remove(db_path)


@pytest_asyncio.fixture
async def session():
    async with SessionLocal() as session:
        async with session.begin() as transaction:
            yield session
            await transaction.rollback()


@pytest_asyncio.fixture
async def product_factory(session):
    async def add_product(name: str, description: str) -> Product:
        product = Product(
            name=name,
            description=description
        )
        session.add(product)
        await session.flush()
        return product
    return add_product