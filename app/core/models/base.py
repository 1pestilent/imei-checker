from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///database.db")
new_session = async_sessionmaker(engine, expire_on_commit=True)

async def get_session():
    async with new_session() as session:
        yield session

async def setup_database():
    from core.models.user import UserModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"Status": True, "Text": "База успешно создана!"}

class Base(AsyncAttrs, DeclarativeBase):
    pass
