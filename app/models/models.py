from sqlalchemy import BigInteger, String, Boolean, ForeignKey, DateTime, text, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_session, async_sessionmaker, create_async_engine

import sqlite3

engine = create_async_engine("sqlite:///database.db")

new_session = async_sessionmaker(engine, expire_on_commit=True)

async def get_session():
    async with new_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[DateTime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())"))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc',now())"))