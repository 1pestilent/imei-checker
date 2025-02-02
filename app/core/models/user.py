from sqlalchemy import BigInteger, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import Base

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    fullname: Mapped[str] = mapped_column(String(63), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))