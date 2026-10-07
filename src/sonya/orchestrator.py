import time
from datetime import datetime
from functools import wraps

from sonya.collectors.telegram.runner import collect_messages
from sonya.collectors.telegram.save import save_html
from sonya.collectors.tg_stat.browser import create_browser
from sonya.collectors.tg_stat.runner import collect_channels
from sonya.database.session import get_session
from sonya.repositories.channels import (
    get_channels_for_inspection,
    save_channels_db,  # type: ignore
)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        excecution_time = end_time - start_time
        print(f"Функция {func.__name__}, выполнялась: {excecution_time}")
        return result

    return wrapper


@timer
def inspect_telegram(limit: int = 20, batch_size: int = 10):
    with get_session() as session:
        channels = get_channels_for_inspection(session, limit)

        for i in range(0, len(channels), batch_size):
            batch = channels[i : i + batch_size]

            for channel in batch:
                try:
                    message_html = collect_messages(channel.url)
                    if isinstance(message_html, str):
                        save_html(channel.id, message_html)
                        channel.private = False

                    else:
                        channel.private = True
                    channel.inspection_date = datetime.now()
                except Exception as e:
                    print(f"Ошибка {channel.url}: {e}")

            session.commit()


@timer
def collect_tgstat(topic: str):
    with create_browser() as browser:
        page = browser.new_page()

        page.goto(
            f"https://tgstat.ru/{topic}",
            wait_until="domcontentloaded",
        )
        channels = collect_channels(page)
        save_channels_db(channels)

        print("Всего уникальных каналов:", len(channels))
