from sonya.collectors.tg_stat.pagination import get_next_page
from sonya.collectors.tg_stat.parse import parse_channels


def collect_channels(page, topic: str, count: int):
    all_channels = set()

    # первая страница
    channels = parse_channels(page.content())
    all_channels.update(channels)
    # остальные страницы
    for page_number in range(2, count + 1):
        response = get_next_page(page, topic)

        if response.status != 200:
            print("Ошибка:", response.text()[:1000])
            break

        data = response.json()  # Получение данных из ответа в формате JSON

        channels = parse_channels(data["html"])
        all_channels.update(channels)

        print(f"Страница {page_number}:", len(channels))

        if not data["hasMore"]:
            print("Страницы закончились.")
            break
    return all_channels
