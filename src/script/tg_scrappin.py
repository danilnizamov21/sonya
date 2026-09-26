from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="./telegram_profile",
        headless=False,
        channel="chrome",
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.telegram.org/a/")

    print("URL:", page.url)
    print("TITLE:", page.title())

    input("Enter для выхода...")

    context.close()