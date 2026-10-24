import logging
import os
import shutil
from pathlib import Path

from sonya.core.parser.pars import parse_messages
from sonya.core.repositories.links import save_links

logger = logging.getLogger(__name__)


def pars_messages() -> None:
    path_dir = Path("src/sonya/storage/html/")
    if not path_dir.exists():
        logger.warning("Directory %s does not exist", path_dir)
        return

    empty_dir = path_dir / "empty"

    for file_path in list(path_dir.iterdir()):
        if not (file_path.is_file() and file_path.suffix == ".html"):
            continue

        try:
            html = file_path.read_text(encoding="utf-8")

            parsed = parse_messages(html)
            if not parsed:
                empty_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), empty_dir / file_path.name)
                logger.info(
                    "HTML file contains no links; moved it to the empty directory"
                )
                continue

            channel_id = int(file_path.stem)
            save_links(channel_id=channel_id, message_list=parsed)

            file_path.unlink()
        except Exception:
            logger.exception("Could not process an HTML file")


def clear_storage(dir_path: str) -> None:

    if not os.path.exists(dir_path):
        logger.warning("Directory %s does not exist", dir_path)
        return

    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
        except Exception:
            logger.exception("Could not remove a storage item")
