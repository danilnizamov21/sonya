def save_html(id: int, message: str) -> None:
    filename = f"src/sonya/storage/html/{id}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)
