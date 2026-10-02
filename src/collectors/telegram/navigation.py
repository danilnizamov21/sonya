from playwright.sync_api import Page


def open_channel(page: Page, channel_url: str):

    # page.on("dialog", lambda dialog: dialog.dismiss())
    page.goto(channel_url)

    web_btn = page.locator("a.tgme_action_web_button")
    web_btn.wait_for(state="visible", timeout=10000)
    web_btn.click()
    page.wait_for_timeout(1000)
