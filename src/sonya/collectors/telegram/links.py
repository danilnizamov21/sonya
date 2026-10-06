from playwright.sync_api import Page


def get_message_container_html(page: Page) -> str:
    return page.locator("div.message-date-group").last.inner_html()
