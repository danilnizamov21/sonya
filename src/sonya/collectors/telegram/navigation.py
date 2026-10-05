from playwright.sync_api import Page


def check_channel_availability(page: Page) -> bool:
    """функция для проверки канала(является ли он публичным)"""
    page.wait_for_load_state()
    page.wait_for_timeout(5000)
    # button_visible = page.locator("text=Request to Join Channel").is_visible()
    # error = page.locator("div.modal-title").filter(has_text="Something went wrong")

    # print("error count:", error.count())
    # print("error visible:", error.is_visible())
    # print("URL:", page.url)

    # print(
    #     "Something count:", page.get_by_text("Something went wrong", exact=True).count()
    # )

    # print("body:")
    # print(page.locator("body").inner_text())
    # print("modal-title:", page.locator("div.modal-title").count())
    message_container = page.locator("div.message-date-group").last.is_visible()
    return message_container


def open_channel(page: Page, channel_url: str):

    page.goto(channel_url, wait_until="domcontentloaded")

    web_btn = page.locator("a.tgme_action_web_button")

    web_btn.click()
    return check_channel_availability(page)
