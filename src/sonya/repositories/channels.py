from sonya.database.models import Channel
from sonya.database.session import get_session


def save_channels_db(channls: list[str]) -> None:

    with get_session() as session:
        for channel_url in channls:
            existing_channel = session.query(Channel).filter_by(url=channel_url).first()
            if not existing_channel:
                new_channel = Channel(url=channel_url)
                session.add(new_channel)
