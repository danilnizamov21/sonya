from bs4 import BeautifulSoup

from sonya.core.utils.channel_url import normalize_channel_url


def parse_channels(html: str) -> list[str]:
    """Парсинг всех ссылок на каналы с полученного HTML"""
    soup = BeautifulSoup(html, "html.parser")
    channels: list[str] = []
    for link in soup.select("a[href]"):
        href = link.get("href")
        if not (isinstance(href, str) and "/channel/" in href):
            continue

        tail = href.rstrip("/").split("/")[-1]

        url = normalize_channel_url(tail if tail.startswith("@") else f"+{tail}")
        if url:
            channels.append(url)
    return channels
