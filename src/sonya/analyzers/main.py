import json
import re

import pymorphy3

KEYWORDS = {
    "казино",
    "слоты",
    "бонус",
    "депозит",
    "бонуска",
    "jetton",
    "деп",
    "фриспин",
}


def get_lemmas(text: str) -> list[str]:
    morph = pymorphy3.MorphAnalyzer()
    words = re.findall(r"[а-яёa-z]+", text)

    normalized_words = []
    for word in words:
        # Анализируем слово
        parsed_word = morph.parse(word)[0]
        # Приводим к начальной форме (именительный падеж, ед. число)
        normal_form = parsed_word.normal_form
        normalized_words.append(normal_form)

    return normalized_words


def find_words(lemm: list[str]):
    return [word for word in lemm if word in KEYWORDS]


path = "src/sonya/storage/json/34.json"
with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Достаем данные по ключу
for item in data:
    count = item["count"]
    text = item["text"]
    lem = get_lemmas(text)
    find = find_words(lem)
    print(find)
    for url in item["urls"]:
        print("1")
