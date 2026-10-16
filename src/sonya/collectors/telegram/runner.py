from sonya.collectors.telegram.browser import create_browser
from sonya.collectors.telegram.links import get_message_container_html
from sonya.collectors.telegram.navigation import open_channel
from sonya.collectors.telegram.status import Status


def collect_messages(channel_url: str):
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()

        check = open_channel(page, channel_url)

        if check != Status.ACCESSIBLE:
            print(f"Канал {channel_url} недоступен: {check}")
            return False

        print(f"Канал {channel_url} доступен")
        return get_message_container_html(page)


# ["private", "long_waiting", "access", "error"]
