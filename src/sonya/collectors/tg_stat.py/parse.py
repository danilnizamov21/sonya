from bs4 import BeautifulSoup


def parse_channels(html:str) -> list[str]:
    """Парсинг всех ссылок на каналы с полученного HTML"""
    soup = BeautifulSoup(html, "html.parser")
    channels = []
    for link in soup.select("a[href]"):
        href = link.get("href")
        if isinstance(href,str) and href and "/channel/" in href:
            normalized_url = normalize_channel_url(href)
            channels.append(normalized_url)
    return channels

def normalize_channel_url(href:str) -> str:
    url = href.rstrip("/").split("/")[-1]
    if url.startswith("@"):
        url = "https://t.me/" + url[1:]
    else:
        url = "https://t.me/joinchat/" + url
    return url