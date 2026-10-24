import logging
from collections.abc import Iterable

from sonya.core.repositories.channels import save_channels_db
from sonya.core.utils.channel_url import normalize_channel_url

logger = logging.getLogger(__name__)


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
        logger.debug("Uploading a channel")
    save_channels_db(channels)
    logger.info("Saved %d channels", len(channels))
    return channels, duplicates
