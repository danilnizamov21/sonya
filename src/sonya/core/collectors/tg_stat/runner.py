import logging

from sonya.core.collectors.tg_stat.pagination import get_next_page
from sonya.core.collectors.tg_stat.parse import parse_channels

logger = logging.getLogger(__name__)


def collect_channels(page, count: int, topic: str):
    all_channels = set()

    # первая страница
    channels = parse_channels(page.content())
    all_channels.update(channels)
    # остальные страницы
    for page_number in range(2, count + 1):
        response = get_next_page(page, topic)

        if response.status != 200:
            logger.error(
                "TGStat returned HTTP status %d", response.status
            )
            break

        data = response.json()  # Получение данных из ответа в формате JSON

        channels = parse_channels(data["html"])
        all_channels.update(channels)

        logger.info("Page %d: collected %d channels", page_number, len(channels))

        if not data["hasMore"]:
            logger.info("No more TGStat pages")
            break
    return all_channels
