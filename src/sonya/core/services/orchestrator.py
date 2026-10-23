from sonya.core.collectors.telegram.status import Status
from sonya.core.services.parsing_service import pars_messages
from sonya.core.services.telegram_service import inspect_telegram
from sonya.core.utils.decorators import timer


@timer
def orchestrator_tg(
    status: Status | None,
    limit: int | None,
    batch_size: int,
):
    inspect_telegram(status=status, limit=limit, batch_size=batch_size)
    pars_messages()
