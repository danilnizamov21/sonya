

import json
from collections.abc import Iterable

from browserforge.fingerprints import Screen
from bs4 import BeautifulSoup
from camoufox.sync_api import Camoufox

MAX_PAGES = 5
def pagination(page):
    """Реализация пагинации на сайте"""
    with page.expect_response(
        lambda response: "/gambling" in response.url
    ) as response_info:

        page.get_by_text("Показать больше").click()

    response = response_info.value

    print("STATUS:", response.status)
    print("URL:", response.url)

    return response

def parse_channels(html:str) -> list[str]:
    """Парсинг всех ссылок на каналы с полученного HTML"""
    soup = BeautifulSoup(html, "html.parser")
    channels = []
    for link in soup.select("a[href]"):
        href = link.get("href")
        if isinstance(href,str) and href and "/channel/" in href:
            normalized_url = normalize_channel_url(href)
            channels.append(normalized_url)
    return channels
    
def get_first_page(page):
    """Получение HTML первой страницы"""
    html = page.content()
    return parse_channels(html)
def save_channels(channels: Iterable[str]) -> None:
    with open("channels.json", "w", encoding="utf-8") as f:
        
        json.dump(
            sorted(channels),
            f,
            ensure_ascii=False,
            indent=4,
        )

def normalize_channel_url(href:str) -> str:
    url = href.rstrip("/").split("/")[-1]
    if url.startswith("@"):
        url = "https://t.me/" + url[1:]
    else:
        url = "https://t.me/joinchat/" + url
    return url
    
constrains = Screen(max_width=1920, max_height=1080)

with Camoufox(
    os="windows",
    screen=constrains,
    persistent_context=True,
    user_data_dir="./camoufox_profile",
    humanize=2.0,
) as browser:

    page = browser.new_page()
    page.goto("https://tgstat.ru/gambling")

    print("Страница:", page.title())

    all_channels = set()
    #первая страница
    channels = get_first_page(page)

    print("Первая страница:", len(channels))
    all_channels.update(channels)
    for channel in channels:
        print(channel)
        

    # след страницы
    for page_number in range(2, MAX_PAGES + 1):
        response = pagination(page)

        if response.status != 200:
            print("Ошибка:", response.text()[:1000])
            break

        data = response.json()

        channels = parse_channels(data["html"])
        all_channels.update(channels)

        print(f"Страница {page_number}:", len(channels))

        for channel in channels:
            print(channel)

        if not data["hasMore"]:
            print("Страницы закончились.")
            break
    save_channels(all_channels)