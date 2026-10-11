from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Message:
    count: int
    urls: list[str]
    text: str


def parse_messages(html: str) -> list[Message]:
    soup = BeautifulSoup(html, "html.parser")
    messages = soup.find_all("div", class_="Message")
    result: list[Message] = []

    for i, message in enumerate(messages):
        text_block = message.find("div", class_="text-content")
        if text_block is None:
            continue

        for delete in text_block.select(".Reactions, .CommentButton"):
            delete.decompose()

        text = text_block.get_text(strip=True, separator=" ")
        text = text.lower()
        clean_links = list(
            {
                str(href)
                for link in text_block.find_all("a")
                if (href := link.get("href")) is not None
            }
        )

        if clean_links:
            item = Message(count=i + 1, urls=clean_links, text=text)
            result.append(item)

    return result
