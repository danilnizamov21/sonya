import os
import shutil
from pathlib import Path

from sonya.parser.pars import parse_messages
from sonya.repositories.links import save_links


def pars_messages() -> None:
    path_dir = Path("src/sonya/storage/html/")
    if not path_dir.exists():
        print(f"Директория {path_dir} не существует.")
        return

    for file_path in path_dir.iterdir():
        if not (file_path.is_file() and file_path.suffix == ".html"):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            parsed = parse_messages(html)
            if parsed:
                channel_id = int(file_path.stem)
                save_links(channel_id=channel_id, message_list=parsed)

            file_path.unlink()
        except Exception as e:
            print(f"Не обработан {file_path}: {e}")


def clear_storage(dir_path: str) -> None:

    if not os.path.exists(dir_path):
        print(f"Директория {dir_path} не существует.")
        return

    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
        except Exception as e:
            print(f"Не удалось удалить {full_path}: {e}")
