from playwright.sync_api import Page


def check_channel_availability(page: Page) -> bool:
    page.wait_for_load_state("domcontentloaded")

    messages = page.locator("div.message-date-group").last

    try:
        messages.wait_for(state="visible", timeout=10000)
        return True

    except TimeoutError:
        print("TIMEOUT")
        print("URL:", page.url)
        print("messages:", page.locator("div.message-date-group").count())
        print("body:")
        print(page.locator("body").inner_text()[:3000])

        return False


def open_channel(page: Page, channel_url: str):

    page.goto(channel_url, wait_until="domcontentloaded")

    web_btn = page.locator("a.tgme_action_web_button")

    web_btn.click()
    return check_channel_availability(page)
