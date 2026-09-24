import time

from browserforge.fingerprints import Screen
from camoufox.sync_api import Camoufox

constrains = Screen(max_width=1920, max_height=1080)
with Camoufox(os="windows", screen=constrains, persistent_context=True,
        user_data_dir="./camoufox_profile",) as browser:
    page = browser.new_page()
    page.goto("https://tgstat.ru/adult")
    time.sleep(240)