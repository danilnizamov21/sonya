import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

load_dotenv(Path(__file__).resolve().parent / ".env")

TG_PROXY_SERVER = os.getenv("TG_PROXY_SERVER")
TG_PROXY_USERNAME = os.getenv("TG_PROXY_USERNAME")
TG_PROXY_PWD = os.getenv("TG_PROXY_PWD")

if not all((TG_PROXY_SERVER, TG_PROXY_USERNAME, TG_PROXY_PWD)):
    raise RuntimeError(
        "TG_PROXY_SERVER, TG_PROXY_USERNAME, TG_PROXY_PWD must be set in .env"
    )

proxy_config = {
    "server": TG_PROXY_SERVER,
    "username": TG_PROXY_USERNAME,
    "password": TG_PROXY_PWD,
}


@contextmanager
def create_browser():
    stealth = Stealth()
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(Path(__file__).resolve().parent / "telegram_profile"),
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-external-intent-requests",
                "--disable-features=ExternalProtocolDialog",
            ],
            proxy=proxy_config,  # type: ignore
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        )
        stealth.apply_stealth_sync(context)
        try:
            yield context
        finally:
            context.close()
