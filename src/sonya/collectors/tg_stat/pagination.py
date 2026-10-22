def get_next_page(page, topic: str):
    """Реализация пагинации на сайте tgstat"""
    with page.expect_response(
        lambda response: f"tgstat.ru/{topic}" in response.url
    ) as response_info:
        page.get_by_text("Показать больше").click()

    return response_info.value