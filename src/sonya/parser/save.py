import json
from dataclasses import asdict

from sonya.parser.pars import Message


def save_messages(channel_id: int, message_list: list[Message]) -> None:
    path = f"src/sonya/storage/json/{channel_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            message_list,
            f,
            indent=4,
            ensure_ascii=False,
            default=lambda o: asdict(o) if isinstance(o, Message) else str(o),
        )
