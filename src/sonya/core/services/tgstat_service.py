import logging

from sonya.core.collectors.tg_stat.browser import create_browser
from sonya.core.collectors.tg_stat.runner import collect_channels
from sonya.core.repositories.channels import (
    save_channels_db,
)
from sonya.core.session.tgstat.tgstat_session import create_sesison_for_tgstat

logger = logging.getLogger(__name__)


def collect_tgstat(topic: str, pages: int = 5):
    logger.info("Starting TGStat collection")
    try:
        with create_browser() as browser:
            page = browser.new_page()

            page.goto(
                f"https://tgstat.ru/{topic}",
                wait_until="domcontentloaded",
            )
            channels = collect_channels(page, topic=topic, count=pages)
            save_channels_db(channels)

            logger.info("Collected %d unique channels", len(channels))
    except Exception:
        logger.exception("TGStat collection failed")
        raise


def login_tgstat():
    try:
        create_sesison_for_tgstat()
    except Exception:
        logger.exception("TGStat login failed")
        raise
