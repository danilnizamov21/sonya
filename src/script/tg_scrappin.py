from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

stealth = Stealth()
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="./telegram_profile",
        headless=False,
        channel="chrome",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-external-intent-requests",
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
    )
    stealth.apply_stealth_sync(context)
    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://t.me")
    page.wait_for_timeout(100000)
    # page.wait_for_timeout(1200)
    # page.keyboard.press("Escape")
    # page.on("dialog", lambda dialog: dialog.dismiss())
    # page.get_by_text("Open in Web").click()
    # div_button = page.get_by_text("Links").first
    # div_button.hover()
    # time.sleep(1.21)
    # div_button.click()
    # page.wait_for_selector("a.site-name", timeout=5000)
    # links_elements = page.locator("a.site-name").all()

    # extracted_urls = []
    # for element in links_elements:
    #     url = element.get_attribute("href")
    #     if url:
    #         extracted_urls.append(url)

    # page.wait_for_timeout(800)

    # print(f"Найдено ссылок: {len(extracted_urls)}")
    # for link in extracted_urls:
    #     print(link)

    input("Enter для выхода...")
    context.close()
