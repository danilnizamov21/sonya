import logging

from playwright.sync_api import Page

from sonya.core.collectors.telegram.links import get_message_container_html
from sonya.core.collectors.telegram.navigation import open_channel
from sonya.core.collectors.telegram.status import Status

logger = logging.getLogger(__name__)


def collect_messages(
    status: Status | None, page: Page, channel_url: str
) -> str | Status:
    if status == Status.ACCESSIBLE:
        result = get_message_container_html(page)
        return result
    else:
        check = open_channel(page, channel_url)

        if check != Status.ACCESSIBLE:
            logger.warning("Channel is unavailable: %s", check)
            return check

        logger.info("Channel is accessible")

        result = get_message_container_html(page)

        if isinstance(result, Status):
            return result

        if isinstance(result, str):
            return result

        return Status.ERROR
