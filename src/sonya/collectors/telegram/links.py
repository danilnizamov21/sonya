from playwright.sync_api import Page


def get_message_container_html(page: Page) -> str:
    try:
        messages = page.locator("div.message-date-group").last
        messages.wait_for(state="visible", timeout=10000)
        return page.locator("div.message-date-group").last.inner_html()
    except TimeoutError:
        print("TIMEOUT")
        print("URL:", page.url)
        print("messages:", page.locator("div.message-date-group").count())
        print("body:")
        print(page.locator("body").inner_text()[:3000])
        return "error"
