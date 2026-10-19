import os
from pathlib import Path

from sonya.parser.pars import parse_messages
from sonya.repositories.links import save_links


def pars_messages() -> None:
    path_dir = Path("src/sonya/storage/html/")
    for file_path in path_dir.iterdir():
        if file_path.is_file() and file_path.suffix == ".html":
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            parsed = parse_messages(html)

            if parsed:
                channel_id = int(file_path.stem)
                save_links(channel_id=channel_id, message_list=parsed)
    clear_storage()


def clear_storage() -> None:
    dir_path = "src/sonya/storage/html/"
    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        if os.path.isfile(full_path):
            os.remove(full_path)
