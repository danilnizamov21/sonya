import logging

from sonya.core.collectors.telegram.browser import create_browser

logger = logging.getLogger(__name__)

QR_SELECTOR = "svg > rect"
PWD_SELECTOR = "#sign-in-password"


def create_session_for_telegram(password: str):
    """создание сесси ТГ"""
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://web.telegram.org/a/")
        try:
            page.wait_for_selector(QR_SELECTOR, timeout=120000)
            page.screenshot(type="png", path="src/sonya/session/qr_for_login.png")
            page.wait_for_selector(PWD_SELECTOR, timeout=120000)

            page.fill(selector=PWD_SELECTOR, value=password)
            page.get_by_role("button", name="Next").click()

            page.press(selector=PWD_SELECTOR, key="Enter")
            page.wait_for_selector(".chat-list")
            logger.info("Telegram session created successfully")
        except Exception:
            logger.exception("Telegram authorization failed")
            raise
