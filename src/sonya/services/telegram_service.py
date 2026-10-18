from datetime import datetime

from sonya.collectors.telegram.runner import collect_messages
from sonya.collectors.telegram.save import save_html
from sonya.collectors.telegram.status import Status
from sonya.database.session import get_session
from sonya.repositories.channels import get_channels_for_inspection


def inspect_telegram(limit: int = 20, batch_size: int = 10):
    with get_session() as session:
        channels = get_channels_for_inspection(session, limit)

        for i in range(0, len(channels), batch_size):
            batch = channels[i : i + batch_size]

            for channel in batch:
                try:
                    result = collect_messages(channel.url)

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
