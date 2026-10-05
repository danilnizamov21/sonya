from playwright.sync_api import Page


def check_channel_availability(page: Page) -> bool:
    """функция для проверки канала(является ли он публичным)"""
    page.wait_for_load_state()
    button_visible = page.locator("text=Request to Join Channel").is_visible()
    error_visible = page.locator("text=Something went wrong").is_visible()
    return button_visible or error_visible


def open_channel(page: Page, channel_url: str):

    page.goto(channel_url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    web_btn = page.locator("a.tgme_action_web_button")
    page.wait_for_timeout(3000)

    web_btn.click()
    return check_channel_availability(page)
