from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    private: Mapped[bool] = mapped_column(nullable=False, default=False)
    inspection_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=func.now()
    )
