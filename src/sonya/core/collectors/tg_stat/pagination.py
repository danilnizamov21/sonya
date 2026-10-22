def get_next_page(page, topic: str):
    """Реализация пагинации на сайте tgstat"""
    with page.expect_response(
        lambda response: f"/{topic}" in response.url
    ) as response_info:
        page.get_by_text("Показать больше").click()

    response = response_info.value

    return response
