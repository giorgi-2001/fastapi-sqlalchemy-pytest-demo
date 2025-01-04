from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import func

from typing import Annotated
from datetime import datetime


DATABASE_URL = "sqlite+aiosqlite:///database.db"


engine = create_async_engine(DATABASE_URL)


SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


created_at = Annotated[
    datetime,
    mapped_column(server_default=func.now())
]

updated_at = Annotated[
    datetime,
    mapped_column(server_default=func.now(), onupdate=datetime.now)
]

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, index=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_nullable = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]