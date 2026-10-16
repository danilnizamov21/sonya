from sonya.collectors.telegram.browser import create_browser


def login_with_tg(url: str):
    """создание сесси ТГ"""
    with create_browser() as context:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        web_btn = page.locator("a.tgme_action_web_button")
        web_btn.click()
        page.wait_for_timeout(5000)
        auth_btn = page.get_by_role("button", name="Авторизоваться").last
        auth_btn.click()
        page.wait_for_timeout(5000)
