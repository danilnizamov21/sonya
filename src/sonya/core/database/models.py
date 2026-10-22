from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sonya.collectors.telegram.status import Status


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=Status.PENDING.value
    )
    inspection_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    priority: Mapped[int] = mapped_column(nullable=False, default=0)


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)


class ChannelLink(Base):
    __tablename__ = "channel_links"

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id"),
        primary_key=True,
    )

    link_id: Mapped[int] = mapped_column(
        ForeignKey("links.id"),
        primary_key=True,
    )
