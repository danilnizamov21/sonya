from sonya.collectors.telegram.browser import create_browser


def login_with_tg(url: str):
    """создание сесси ТГ"""
    with create_browser() as context:
        print("создаем сессию", flush=True)
        try:
            page = context.pages[0] if context.pages else context.new_page()

            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            page.get_by_text("Open in Web").click()

            messages = page.locator("div.message-date-group").last

            messages.wait_for(state="visible", timeout=40000)
            page.wait_for_timeout(1000)

            auth_btn = page.get_by_role("button", name="Авторизоваться").last
            auth_btn.click()
            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"ОШИБКА: {e}", flush=True)
