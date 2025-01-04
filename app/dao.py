from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy import delete, update
from .database import SessionLocal, Base
from .models import Product


class Dao:
    model: Base = None
    SessionLocal: async_sessionmaker[AsyncSession] = None

    @classmethod
    async def get_all_items(cls):
        async with cls.SessionLocal() as session:
            query = select(cls.model).offset(0).limit(None)
            items = await session.execute(query)
            result = items.scalars().all()
            return result
        
    @classmethod
    async def get_one_or_none(cls, id: int):
        async with cls.SessionLocal() as session:
            query = select(cls.model).filter(cls.model.id==id)
            result = await session.execute(query)
            product = result.scalar_one_or_none()
            return product
        
    @classmethod
    async def add_item(cls, **kwargs):
        async with cls.SessionLocal() as session:
            async with session.begin():
                item = cls.model(**kwargs)

                try:
                    session.add(item)
                    await session.commit()
                except SQLAlchemyError:
                    raise

            await session.refresh(item)
            return item.id
        
    @classmethod
    async def remove_item(cls, id: int):
        async with cls.SessionLocal() as session:
            async with session.begin():
                query = select(cls.model).where(cls.model.id==id)
                result = await session.execute(query)
                product = result.scalar_one_or_none()

                if not product:
                    return None
                
                query = delete(cls.model).where(cls.model.id==id)
                await session.execute(query)
                await session.commit()
            
            return product.id

    @classmethod
    async def update_item(cls, id: int, **kwargs):
        async with cls.SessionLocal() as session:
            async with session.begin():
                query = select(cls.model).where(cls.model.id==id)
                result = await session.execute(query)
                product = result.scalar_one_or_none()

                if not product:
                    return None
                
                query = (
                    update(cls.model)
                    .where(cls.model.id==id)
                    .values(**kwargs)
                )

                try:
                    await session.execute(query)
                    await session.commit()
                except SQLAlchemyError:
                    raise

            await session.refresh(product)
            return product.id

        

class ProductDao(Dao):
    model = Product
    SessionLocal = SessionLocal
