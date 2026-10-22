from contextlib import contextmanager
from pathlib import Path

from browserforge.fingerprints import Screen
from camoufox.sync_api import Camoufox


@contextmanager
def create_browser():
    screen = Screen(
        max_width=1920,
        max_height=1080,
    )

    with Camoufox(
        os="windows",
        screen=screen,
        persistent_context=True,
        user_data_dir=str(Path(__file__).resolve().parent / "camoufox_profile"),
        humanize=2.0,
    ) as browser:
        yield browser
