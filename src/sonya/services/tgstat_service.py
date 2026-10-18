from sonya.collectors.tg_stat.browser import create_browser
from sonya.collectors.tg_stat.runner import collect_channels
from sonya.repositories.channels import (
    save_channels_db,
)


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
