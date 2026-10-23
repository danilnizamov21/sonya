from collections.abc import Iterable

from sonya.core.repositories.channels import save_channels_db
from sonya.core.utils.channel_url import normalize_channel_url


def upload(raw_channels: Iterable[str]):
    seen = set()
    channels = []
    duplicates = []

    for channel in raw_channels:
        key = normalize_channel_url(channel)
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
