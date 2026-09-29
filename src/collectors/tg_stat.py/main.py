import json
from collections.abc import Iterable

from browser import create_browser  # type: ignore
from runner import collect_channels  # type: ignore


def save_channels(channels: Iterable[str]) -> None:
    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(
            sorted(channels),
            f,
            ensure_ascii=False,
            indent=4,
        )


with create_browser() as browser:
    page = browser.new_page()

    page.goto("https://tgstat.ru/gambling")
    channels = collect_channels(page)
    save_channels(channels)

    print("Всего уникальных каналов:", len(channels))
