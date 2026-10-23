from collections.abc import Iterable

from sonya.core.collectors.telegram.status import Status
from sonya.core.database.models import Channel
from sonya.core.database.session import get_session
from sonya.core.utils.channel_url import normalize_channel_url


def save_channels_db(urls: Iterable[str]) -> None:
    with get_session() as session:
        for raw in urls:
            channel_url = normalize_channel_url(raw)
            if channel_url is None:
                continue
            if session.query(Channel).filter_by(url=channel_url).first():
                print("NOT UNIQUE")
                continue
            session.add(Channel(url=channel_url))


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
