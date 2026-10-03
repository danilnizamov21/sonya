from collectors.telegram.browser import create_browser
from collectors.telegram.links import get_message_container_html
from collectors.telegram.navigation import open_channel


def collect_messages(channel_url: str):
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()

        if open_channel(page, channel_url):
            return "приватный канал"

        return get_message_container_html(page)


def main():
    a = collect_messages("https://t.me/joinchat/lAydIhb1ZxpiYTgy")
    with open("tg.html", "w", encoding="utf-8") as f:
        f.write(a)
    print("записано")


if __name__ == "__main__":
    main()
