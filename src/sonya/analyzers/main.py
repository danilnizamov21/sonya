import json

# Открываем файл с указанием кодировки utf-8
path = "src/sonya/storage/json/23.json"
with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Достаем данные по ключу
for item in data:
    count = item["count"]
    text = item["text"]
    for url in item["urls"]:
        print(f"счет: {count}\nсообщение:{text}\nссылка: {url}\n\n")
