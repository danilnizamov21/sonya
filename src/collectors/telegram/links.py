from playwright.sync_api import Page


def collect_links(page: Page):
    div_button = page.get_by_text("Links").first
    div_button.hover()
    page.wait_for_timeout(1210)
    div_button.click()
    page.wait_for_selector("a.site-name", timeout=5000)
    links_elements = page.locator("a.site-name").all()

    extracted_urls = []
    for element in links_elements:
        url = element.get_attribute("href")
        if url:
            extracted_urls.append(url)

    return extracted_urls
