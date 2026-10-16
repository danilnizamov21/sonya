from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sonya.collectors.telegram.status import Status


def check_channel_availability(page: Page) -> Status:
    try:
        page.wait_for_load_state("domcontentloaded")

        billet = page.locator("text=Request to Join Channel")

        if billet.is_visible():
            return Status.PRIVATE

        messages = page.locator("div.message-date-group").last

        try:
            messages.wait_for(state="visible", timeout=40000)
            return Status.ACCESSIBLE
        except PlaywrightTimeoutError:
            return Status.TIMEOUT

    except Exception:
        return Status.ERROR


def open_channel(page: Page, channel_url: str) -> Status:

    page.goto(channel_url, wait_until="domcontentloaded")

    web_btn = page.locator("a.tgme_action_web_button")

    web_btn.click()
    return check_channel_availability(page)
