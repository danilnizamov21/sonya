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


def get_channels_for_inspection(
    session,
    status: Status | None = None,
    limit: int | None = 20,
):
    query = session.query(Channel)

    if status is not None:
        query = query.filter(Channel.status == status.value)

    query = query.order_by(
        Channel.priority.desc(),
        Channel.inspection_date.asc().nullsfirst(),
    )
    if limit is not None:
        query = query.limit(limit)
    return query.all()
