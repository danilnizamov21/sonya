import time
from datetime import datetime
from functools import wraps
from pathlib import Path

from sonya.collectors.telegram.runner import collect_messages
from sonya.collectors.telegram.save import save_html
from sonya.collectors.telegram.status import Status
from sonya.collectors.tg_stat.browser import create_browser
from sonya.collectors.tg_stat.runner import collect_channels
from sonya.database.session import get_session
from sonya.parser.pars import parse_messages
from sonya.repositories.channels import (
    get_channels_for_inspection,
    save_channels_db,
)
from sonya.repositories.links import save_messages_bd


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


@timer
def collect_tgstat(topic: str):
    with create_browser() as browser:
        page = browser.new_page()

        page.goto(
            f"https://tgstat.ru/{topic}",
            wait_until="domcontentloaded",
        )
        channels = collect_channels(page, 5)
        save_channels_db(channels)

        print("Всего уникальных каналов:", len(channels))


@timer
def pars_messages() -> None:
    path_dir = Path("src/sonya/storage/html/")
    for file_path in path_dir.iterdir():
        if file_path.is_file() and file_path.suffix == ".html":
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            parsed = parse_messages(html)

            if parsed:
                channel_id = int(file_path.stem)
                save_messages_bd(channel_id=channel_id, message_list=parsed)
