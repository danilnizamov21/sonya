from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def check_channel_availability(page: Page) -> bool:
    page.wait_for_load_state("domcontentloaded")

    messages = page.locator("div.message-date-group").last

    try:
        messages.wait_for(state="visible", timeout=10000)
        return True

    except PlaywrightTimeoutError:
        return False


def open_channel(page: Page, channel_url: str) -> bool:

    page.goto(channel_url, wait_until="domcontentloaded")

    web_btn = page.locator("a.tgme_action_web_button")

    web_btn.click()
    return check_channel_availability(page)
