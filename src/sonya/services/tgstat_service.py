from sonya.collectors.tg_stat.browser import create_browser
from sonya.collectors.tg_stat.runner import collect_channels
from sonya.repositories.channels import (
    save_channels_db,
)
from sonya.session.tgstat.tgstat_session import create_sesison_for_tgstat


def collect_tgstat(topic: str, pages: int = 5):
    with create_browser() as browser:
        page = browser.new_page()

        page.goto(
            f"https://tgstat.ru/{topic}",
            wait_until="domcontentloaded",
        )
        channels = collect_channels(page, topic=topic, count=pages)
        save_channels_db(channels)

        print("Всего уникальных каналов:", len(channels))


def login_tgstat():
    create_sesison_for_tgstat()
