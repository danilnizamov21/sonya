from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sonya.collectors.telegram.status import Status

import re

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sonya.collectors.telegram.status import Status

LOAD_TIMEOUT_MS = 40_000


def check_channel_availability(page: Page) -> Status:
    try:
        page.wait_for_load_state("domcontentloaded")

        error_banner = page.get_by_text(re.compile(r"something went wrong", re.I))
        join_button = page.get_by_role(
            "button", name=re.compile(r"request to join", re.I)
        )
        messages = page.locator("div.message-date-group").last

        
        first = error_banner.or_(join_button).or_(messages).first
        first.wait_for(state="visible", timeout=LOAD_TIMEOUT_MS)

        if error_banner.first.is_visible() or join_button.first.is_visible():
            return Status.PRIVATE

        return Status.ACCESSIBLE

    except PlaywrightTimeoutError:
        return Status.TIMEOUT
    except Exception:
        return Status.ERROR

def open_channel(page: Page, channel_url: str) -> Status:
    page.goto(channel_url, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    page.get_by_text("Open in Web").click()

    # web_btn = page.locator("a.tgme_action_web_button")

    # web_btn.click()

    return check_channel_availability(page)
