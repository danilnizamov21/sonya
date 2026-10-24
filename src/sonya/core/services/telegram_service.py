import logging
from datetime import datetime

from sonya.core.collectors.telegram.browser import create_browser
from sonya.core.collectors.telegram.runner import collect_messages
from sonya.core.collectors.telegram.save import save_html
from sonya.core.collectors.telegram.status import Status
from sonya.core.database.session import get_session
from sonya.core.repositories.channels import get_channels_for_inspection
from sonya.core.session.telegram_session import create_session_for_telegram

logger = logging.getLogger(__name__)


def inspect_telegram(
    status: Status | None,
    limit: int | None = 20,
    batch_size: int = 10,
) -> None:
    logger.info("Starting Telegram channel inspection")
    with get_session() as session:
        channels = get_channels_for_inspection(session, status, limit)
        if not channels:
            return

        try:
            with create_browser() as context:
                page = context.pages[0] if context.pages else context.new_page()

                for i in range(0, len(channels), batch_size):
                    batch = channels[i : i + batch_size]

                    for channel in batch:
                        try:
                            result = collect_messages(status, page, channel.url)

                            if isinstance(result, Status):
                                channel.status = result.value
                            elif isinstance(result, str):
                                save_html(channel.id, result)
                                channel.status = Status.ACCESSIBLE.value
                            else:
                                channel.status = Status.ERROR.value

                        except Exception:
                            logger.exception("Failed to inspect a Telegram channel")
                            channel.status = Status.ERROR.value

                        finally:
                            channel.inspection_date = datetime.now()

                    session.commit()
        except Exception:
            logger.exception("Telegram inspection failed")
            raise


def login_telegram(password):
    create_session_for_telegram(password)
