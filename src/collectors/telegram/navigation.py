import time

from playwright.sync_api import Page


def open_channel(page: Page, channel_url: str):
    page.goto(channel_url)
    time.sleep(1000)

    # page.on("dialog", lambda dialog: dialog.dismiss())
    # page.wait_for_timeout(1200)
    # page.get_by_text("Open in Web").click()
