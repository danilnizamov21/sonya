def get_next_page(page):
    """Реализация пагинации на сайте tgstat"""
    with page.expect_response(
        lambda response: "/gambling" in response.url
    ) as response_info:

        page.get_by_text("Показать больше").click()

    response = response_info.value

    return response