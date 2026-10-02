from bs4 import BeautifulSoup

with open("tg.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
    messages = soup.find_all("div", class_="Message")

    for message in messages:
        text_block = message.find("div", class_="text-content")

        if text_block:
            for delete in text_block.select(".Reactions, .CommentButton"):
                delete.decompose()
            text = text_block.get_text(separator="\n", strip=True)
            links = text_block.find_all("a")
            clean_links_set = set()

            for link in links:
                href = link.get("href")
                if href is not None:
                    clean_links_set.add(str(href))

            clean_links = list(clean_links_set)

            if clean_links and text:
                print(f"ссылки: {clean_links}")
                print(f"сообщение:\n{text}")
                print("=================================")
