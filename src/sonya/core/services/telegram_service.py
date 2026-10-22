from datetime import datetime

from sonya.core.collectors.telegram.browser import create_browser
from sonya.core.collectors.telegram.runner import collect_messages
from sonya.core.collectors.telegram.save import save_html
from sonya.core.collectors.telegram.status import Status
from sonya.core.database.session import get_session
from sonya.core.repositories.channels import get_channels_for_inspection
from sonya.core.session.telegram_session import create_session_for_telegram


def inspect_telegram(limit: int = 20, batch_size: int = 10) -> None:
    with get_session() as session:
        channels = get_channels_for_inspection(session, limit)
        if not channels:
            return

        with create_browser() as context:
            page = context.pages[0] if context.pages else context.new_page()

            for i in range(0, len(channels), batch_size):
                batch = channels[i : i + batch_size]

                for channel in batch:
                    try:
                        result = collect_messages(page, channel.url)

                        if isinstance(result, Status):
                            channel.status = result.value
                        elif isinstance(result, str):
                            save_html(channel.id, result)
                            channel.status = Status.ACCESSIBLE.value
                        else:
                            channel.status = Status.ERROR.value

                    except Exception as e:
                        print(f"Ошибка {channel.url}: {e}")
                        channel.status = Status.ERROR.value

                    finally:
                        channel.inspection_date = datetime.now()

                session.commit()


def login_telegram(password):
    create_session_for_telegram(password)
