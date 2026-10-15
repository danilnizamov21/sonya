from sonya.collectors.telegram.browser import create_browser


def login_with_tg(url: str):
    """создание сесси ТГ"""
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url)
        page.pause()
