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
        