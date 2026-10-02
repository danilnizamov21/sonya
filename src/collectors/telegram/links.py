from playwright.sync_api import Page


def get_message_container_html(page: Page):
    page.wait_for_timeout(5000)
    return page.locator("div.message-date-group").last.inner_html()
