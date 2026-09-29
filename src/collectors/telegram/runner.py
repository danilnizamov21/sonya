from collectors.telegram.browser import create_browser
from collectors.telegram.links import collect_links
from collectors.telegram.navigation import open_channel


def collect_channel_links(channel_url: str):
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()

        open_channel(page, channel_url)

        return collect_links(page)


def main():
    a = collect_channel_links("https://t.me/ALOHADANCEya")
    for item in a:
        print(item)


if __name__ == "__main__":
    main()
