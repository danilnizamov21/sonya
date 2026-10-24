import logging
from concurrent.futures import ThreadPoolExecutor

from sonya.core.collectors.tg_stat.browser import create_browser
from sonya.core.session.tgstat.confirm import login_with_tg

logger = logging.getLogger(__name__)

url = None


def new_page(page):
    global url
    logger.info("Starting TGStat Telegram authorization in a worker thread")
    with ThreadPoolExecutor(max_workers=1) as exec:
        exec.submit(login_with_tg, page.url)


def create_sesison_for_tgstat():
    with create_browser() as browser:
        page = browser.new_page()

        browser.on("page", new_page)  # type: ignore

        page.goto("https://tgstat.ru/", timeout=60000, wait_until="domcontentloaded")
        page.get_by_text("Вход на сайт").click()
        page.get_by_text("Войти через Telegram").click()
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Войти через Telegram").click()
        page.wait_for_timeout(5000)
