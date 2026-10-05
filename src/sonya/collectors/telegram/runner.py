from sonya.collectors.telegram.browser import create_browser
from sonya.collectors.telegram.links import get_message_container_html
from sonya.collectors.telegram.navigation import open_channel


def collect_messages(channel_url: str) -> str | bool:
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()
        check = open_channel(page, channel_url)
        if check is False:
            print(f"Канал {channel_url} недоступен")
            return False
        else:
            print(f"Канал {channel_url} доступен")
            return get_message_container_html(page)
