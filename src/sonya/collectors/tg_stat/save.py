import json
from collections.abc import Iterable


def save_channels(channels: Iterable[str]) -> None:
    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(
            sorted(channels),
            f,
            ensure_ascii=False,
            indent=4,
        )
