from playwright.sync_api import Page


def check_channel_availability(page: Page) -> bool:
    """функция для проверки канала(является ли он публичным)"""
    page.wait_for_load_state()
    button_visible = page.locator("text=Request to Join Channel").is_visible()
    error_visible = page.locator("text=Something went wrong").is_visible()
    return not (button_visible or error_visible)


def open_channel(page: Page, channel_url: str):

    # page.on("dialog", lambda dialog: dialog.dismiss())
    page.goto(channel_url)

    web_btn = page.locator("a.tgme_action_web_button")
    web_btn.wait_for(state="visible", timeout=10000)
    web_btn.click()
    return check_channel_availability(page)
