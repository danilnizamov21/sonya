from contextlib import contextmanager

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


@contextmanager
def create_browser():
    stealth = Stealth()
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./telegram_profile",
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-external-intent-requests",
                "--disable-features=ExternalProtocolDialog",
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        )
        stealth.apply_stealth_sync(context)

        yield context

        context.close()
