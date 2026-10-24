import logging

from sonya.core.collectors.telegram.browser import create_browser

logger = logging.getLogger(__name__)


def login_with_tg(url: str):
    """создание сесси ТГ"""
    with create_browser() as context:
        logger.info("Starting Telegram authorization for TGStat")
        try:
            page = context.pages[0] if context.pages else context.new_page()

            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            page.get_by_text("Open in Web").click()

            messages = page.locator("div.message-date-group").last

            messages.wait_for(state="visible", timeout=40000)
            page.wait_for_timeout(1000)

            auth_btn = page.get_by_role("button", name="Авторизоваться").last
            auth_btn.click()
            page.wait_for_timeout(5000)

        except Exception:
            logger.exception("Telegram authorization for TGStat failed")
            raise
