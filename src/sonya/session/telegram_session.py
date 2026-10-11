from sonya.collectors.telegram.browser import create_browser


def create_session_for_telegram():
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.telegram.org/a/")
        page.pause()
        print("gotovo")


def main():
    create_session_for_telegram()


if __name__ == "__main__":
    main()
