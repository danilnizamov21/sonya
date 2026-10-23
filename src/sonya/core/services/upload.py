import re
from collections.abc import Iterable

from sonya.core.repositories.channels import save_channels_db


def normalize_channel(link: str) -> str:

    link = link.strip().lower()
    link = re.sub(r"^https?://", "", link)
    link = re.sub(r"^(t\.me|telegram\.me)/", "", link)
    link = re.sub(r"^@", "", link)
    link = link.rstrip("/")
    return link


def upload(raw_channels: Iterable[str]):
    seen = set()
    channels = []
    duplicates = []

    for channel in raw_channels:
        key = normalize_channel(channel)
        if key in seen:
            duplicates.append(channel)
            continue
        seen.add(key)
        channels.append(key)

    for channel in channels:
        print(channel)
    save_channels_db(channels)
    print("SAVE")
    return channels, duplicates
