from sonya.collectors.tg_stat.browser import create_browser
from sonya.session.tgstat.confirm import login_with_tg

url = None


def new_page(page):
    global url
    url = page.url


def create_sesison_for_tgstat():
    with create_browser() as browser:
        page = browser.new_page()

        browser.on("page", new_page)  # type: ignore

        page.goto("https://tgstat.ru/")
        page.get_by_text("Вход на сайт").click()
        page.get_by_text("Войти через Telegram").click()
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Войти через Telegram").click()
        page.wait_for_timeout(3000)


# <a class="tgme_action_button_new shine" href="tg://resolve?domain=tg_analytics_bot&amp;start=login_VfITyhkNVSg0R1ko1tx6U-MdNCJZGjru">Start Bot</a>
if __name__ == "__main__":
    create_sesison_for_tgstat()
    if url:
        login_with_tg(url)
    else:
        print("Ссылка для авторизации не найдена")
