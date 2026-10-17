from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sonya.collectors.telegram.status import Status


def check_channel_availability(page: Page) -> Status:
    try:
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)

        private = page.get_by_text("Something went wrong", exact=True)
        billet = page.get_by_role("button", name="Request to Join Channel")

        if private.is_visible() or billet.is_visible():
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

    page.wait_for_timeout(3000)

    return check_channel_availability(page)
