import time

from browserforge.fingerprints import Screen
from bs4 import BeautifulSoup
from camoufox.sync_api import Camoufox

constrains = Screen(max_width=1920, max_height=1080)
def pagination(page):
    with page.expect_response(
        lambda response: "/adult" in response.url
    ) as response_info:

        page.get_by_text("Показать больше").click()

    response = response_info.value

    print("STATUS:", response.status)
    print("URL:", response.url)

    return response

def parse_channels(html):
    soup = BeautifulSoup(html, "html.parser")
    chanels = []
    for link in soup.select("a[href]"):
        href = link.get("href")
        if href and "/channel/" in href:
            chanels.append(href)
    return chanels
    
def get_first_page(page):
    html = page.content()
    return parse_channels(html)

with Camoufox(
    os="windows",
    screen=constrains,
    persistent_context=True,
    user_data_dir="./camoufox_profile",
    humanize=2.0,
) as browser:

    page = browser.new_page()
    page.goto("https://tgstat.ru/adult")
    print("Страница:", page.title())
    channels = get_first_page(page)
    print("Первая страница:", len(channels))
    for channel in channels:
        print(channel)

    

    next_page = True
    i = 0
    while next_page:

        response = pagination(page)

        if response.status != 200:
            print(response.text()[:1000])
            break

        data = response.json()

        channels = parse_channels(data["html"])

        print("Следующая страница:", len(channels))

        for channel in channels:
            print(channel)
        i+=1
        if not data["hasMore"] or i == 4: 
            next_page = False