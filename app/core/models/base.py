from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///database.db")

async_session = sessionmaker(engine,
                            class_=AsyncSession,
                            expire_on_commit=False
                            )


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
    
async def setup_database():
    from core.models.user import UserModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"Status": True, "Text": "База успешно создана!"}
class Base(AsyncAttrs, DeclarativeBase):
    pass
