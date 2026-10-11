from sqlalchemy import select

from sonya.database.models import ChannelLink, Link
from sonya.database.session import get_session
from sonya.parser.pars import Message


def save_messages_bd(channel_id: int, message_list: list[Message]) -> None:
    urls = {url for message in message_list for url in message.urls}
    with get_session() as session:
        for url in urls:
            link = session.scalar(select(Link).where(Link.url == url))
            if link is None:
                link = Link(url=url)
                session.add(link)
                session.flush()
            channel_link = session.get(ChannelLink, (channel_id, link.id))
            if channel_link is None:
                channel_link = ChannelLink(
                    channel_id=channel_id,
                    link_id=link.id,
                )
                session.add(channel_link)

            print(f"URL: {url}, ID: {channel_id}")
