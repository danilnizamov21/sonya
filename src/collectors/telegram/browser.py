from contextlib import contextmanager

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


@contextmanager
def create_browser():
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir="./telegram_profile",
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
        )

        Stealth().apply_stealth_sync(context)

        yield context

        context.close()
