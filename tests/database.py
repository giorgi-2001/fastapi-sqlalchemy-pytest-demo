from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from pathlib import Path


db_path = Path(__file__).parent / "test_database.db"


DATABASE_URL = "sqlite+aiosqlite:///" + str(db_path.resolve())


engine = create_async_engine(DATABASE_URL)


SessionLocal = async_sessionmaker(bind=engine, autoflush=False)
