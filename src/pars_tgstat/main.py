import time

from browserforge.fingerprints import Screen
from camoufox.sync_api import Camoufox

constrains = Screen(max_width=1920, max_height=1080)
with Camoufox(os="windows", screen=constrains, persistent_context=True,
        user_data_dir="./camoufox_profile",humanize=2.0) as browser:
        page = browser.new_page()

        page.goto("https://tgstat.ru/pics")

        print("Страница:", page.title())

        with page.expect_response(
            lambda response: "/pics/items" in response.url
        ) as response_info:

            page.get_by_text("Показать больше").click()

        response = response_info.value

        print("STATUS:", response.status)
        print("URL:", response.url)

        if response.status == 200:
            data = response.json()

            print("hasMore:", data["hasMore"])
            print("nextPage:", data["nextPage"])
            print("nextOffset:", data["nextOffset"])
            print(data["html"][:500])
        else:
            print(response.text()[:1000])