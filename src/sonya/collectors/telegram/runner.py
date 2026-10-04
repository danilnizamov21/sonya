from sonya.collectors.telegram.browser import create_browser
from sonya.collectors.telegram.links import get_message_container_html
from sonya.collectors.telegram.navigation import open_channel


def collect_messages(channel_url: str):
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()

        if open_channel(page, channel_url):
            return "ПРИВАТНЫЙ КАНАЛ"
        else:
            return get_message_container_html(page)


def main():
    channels = ["https://t.me/joinchat/ScL1FOCgJCbFNJK1"]
    for idx, channel in enumerate(channels):
        message_html = collect_messages(channel)

        filename = f"{idx}.html"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(message_html)

        print("записано")


if __name__ == "__main__":
    main()
