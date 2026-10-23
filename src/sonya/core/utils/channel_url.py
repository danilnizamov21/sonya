import re

_PREFIX = re.compile(r"^(?:https?://)?(?:www\.)?(?:t\.me|telegram\.me)/", re.IGNORECASE)


def normalize_channel_url(raw: str) -> str | None:
    """Любой вид ссылки -> https://t.me/{username} или https://t.me/joinchat/{id}."""
    value = _PREFIX.sub("", raw.strip()).split("?")[0].rstrip("/")
    if value.lower().startswith("joinchat/"):
        return "https://t.me/joinchat/" + value[9:]
    if value.startswith("+"):
        return "https://t.me/joinchat/" + value[1:]
    value = value.lstrip("@").lower()
    return f"https://t.me/{value}" if value else None
