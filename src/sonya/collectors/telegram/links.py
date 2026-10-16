from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sonya.collectors.telegram.status import Status


def get_message_container_html(page: Page) -> str | Status:
    try:
        messages = page.locator("div.message-date-group").last
        messages.wait_for(state="visible", timeout=40000)
        return page.locator("div.message-date-group").last.inner_html()
    except PlaywrightTimeoutError as e:
        print(f"Таймаут при загрузке сообщений {page.url}: {e}")
        return Status.TIMEOUT
