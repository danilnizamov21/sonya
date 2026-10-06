import time
from datetime import datetime
from functools import wraps

from sonya.collectors.telegram.runner import collect_messages
from sonya.database.session import get_session
from sonya.repositories.channels import get_channels_for_inspection


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
def main(limit: int = 20, batch_size: int = 10):
    with get_session() as session:
        channels = get_channels_for_inspection(session, limit)

        for i in range(0, len(channels), batch_size):
            batch = channels[i : i + batch_size]

            for channel in batch:
                try:
                    message_html = collect_messages(channel.url)
                    if isinstance(message_html, str):
                        filename = f"src/sonya/storage/html/{channel.id}.html"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(message_html)
                        channel.private = False

                    else:
                        channel.private = True
                    channel.inspection_date = datetime.now()
                except Exception as e:
                    print(f"Ошибка {channel.url}: {e}")

            session.commit()


if __name__ == "__main__":
    main()
