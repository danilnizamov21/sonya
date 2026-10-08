from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def get_message_container_html(page: Page) -> str | bool:
    try:
        messages = page.locator("div.message-date-group").last
        messages.wait_for(state="visible", timeout=10000)
        return page.locator("div.message-date-group").last.inner_html()
    except PlaywrightTimeoutError as e:
        print(f"Таймаут при загрузке сообщений {page.url}: {e}")
        return False
