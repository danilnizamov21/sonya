from playwright.sync_api import Page

from sonya.collectors.telegram.links import get_message_container_html
from sonya.collectors.telegram.navigation import open_channel
from sonya.collectors.telegram.status import Status


def collect_messages(page: Page, channel_url: str) -> str | Status:
    check = open_channel(page, channel_url)

    if check != Status.ACCESSIBLE:
        print(f"Канал {channel_url} недоступен: {check}")
        return check

    print(f"Канал {channel_url} доступен")

    result = get_message_container_html(page)

    if isinstance(result, Status):
        return result

    if isinstance(result, str):
        return result

    return Status.ERROR
