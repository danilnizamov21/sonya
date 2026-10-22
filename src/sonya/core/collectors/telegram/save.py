from pathlib import Path


def save_html(id: int, message: str) -> None:
    path = Path("src/sonya/storage/html") / f"{id}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message, encoding="utf-8")
