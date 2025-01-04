# Example of Async FastAPI - SQLalchemy - Pytest setup for efficient testing

In this demonstration project we try to test simple fastapi app using pytest

## Main chanllanges:
- Async logic which is not straightforward to test
- Must not modify actual database state
- Database dependency handling for FastAPI

## Accomplished:
- Unit tests for database model

## Upcomming:
- Integration tests for api routes

## Setup example:
### Defining main fixtures

``` python
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
        
```

### Actual test casis:

```python
    import pytest
    from sqlalchemy.exc import IntegrityError


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name, description, valid", [
            ("Hair Gell", "Very good hair gell", True),
            ("Hair Gell", None, True),
            ("Hair Gell", "", True),
            ("", "Very good hair gell", False),
            (None, "Very good hair gell", False),
        ]
    )
    async def test_product(product_factory, name, description, valid):
        if not valid:
            with pytest.raises(IntegrityError):
                await product_factory(name, description)
        else:
            product = await product_factory(name, description)
            assert product.id == 1
            assert product.name == name
            assert product.description == description


    @pytest.mark.asyncio
    async def test_dublicate_names(product_factory):
        await product_factory("foo", "baz")
        
        with pytest.raises(IntegrityError):
            await product_factory("foo", "baz")

```