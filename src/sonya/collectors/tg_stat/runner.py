from parse import parse_channels  # type: ignore


def collect_channels(page):
    all_channels = set()

    # первая страница
    channels = parse_channels(page.content())
    all_channels.update(channels)

    # остальные страницы
    # for page_number in range(2, 5 + 1):
    #     response = get_next_page(page)

    #     if response.status != 200:
    #         print("Ошибка:", response.text()[:1000])
    #         break

    #     data = response.json() #Получение данных из ответа в формате JSON

    #     channels = parse_channels(data["html"])
    #     all_channels.update(channels)

    #     print(f"Страница {page_number}:", len(channels))

    #     if not data["hasMore"]:
    #         print("Страницы закончились.")
    #         break

    return all_channels
