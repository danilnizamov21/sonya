from collections.abc import Iterable

from sonya.collectors.telegram.status import Status
from sonya.database.models import Channel
from sonya.database.session import get_session


def save_channels_db(channls: Iterable[str]) -> None:

    with get_session() as session:
        for channel_url in channls:
            existing_channel = session.query(Channel).filter_by(url=channel_url).first()
            if not existing_channel:
                new_channel = Channel(url=channel_url)
                session.add(new_channel)
            else:
                print("NOT UNIQUE")


def get_channels_for_inspection(session, limit: int = 20):
    return (
        session.query(Channel)
        .filter(
            Channel.status.in_(
                [
                    Status.PENDING.value,
                    Status.ACCESSIBLE.value,
                    Status.TIMEOUT.value,
                    Status.ERROR.value,
                ]
            )
        )
        .order_by(
            Channel.priority.desc(),
            Channel.inspection_date.asc().nullsfirst(),
        )
        .limit(limit)
        .all()
    )
