from sqlalchemy import BigInteger, String, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import sqlite3

engine = create_async_engine("sqlite+aiosqlite:///database.db")


new_session = async_sessionmaker(engine, expire_on_commit=True)


async def get_session():
    async with new_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(BigInteger, primary_key=True, nullable=False)
    tg_nick: Mapped[str] = mapped_column(String(32), nullable=False)
    firts_name: Mapped[str] = mapped_column(String(32), nullable=False)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=False)


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"Status": True, "Text": "База успешно создана!"}