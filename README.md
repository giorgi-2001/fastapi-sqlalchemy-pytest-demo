# Example of Async FastAPI - SQLalchemy - Pytest setup for efficient testing

In this demonstration project we try to test simple fastapi app using pytest

## Main chanllanges:
- Async logic which is not straightforward to test
- Must not modify actual database state
- Database dependency handling for FastAPI

## Accomplished:
- Unit tests for database model
- Integration tests for API

## Setup example:

``` python
    import pytest
    import pytest_asyncio
    from fastapi.testclient import TestClient

    from app.models import Product
    from app.dao import ProductDao
    from app.main import app
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


    @pytest.fixture
    def client():
        class TestProductDao(ProductDao):
            SessionLocal = SessionLocal

        app.dependency_overrides[ProductDao] = TestProductDao
        client = TestClient(app)

        yield client

        app.dependency_overrides[TestProductDao] = ProductDao



    @pytest.fixture
    def product_data():
        def data(name, description):
            return {
                "name": name,
                "description": description
            }
        return data
        
```