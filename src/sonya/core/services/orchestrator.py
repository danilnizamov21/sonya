from sonya.core.services.parsing_service import pars_messages
from sonya.core.services.telegram_service import inspect_telegram
from sonya.core.utils.decorators import timer


@timer
def orchestrator_tg(limit: int, batch_size: int):
    inspect_telegram(limit, batch_size)
    pars_messages()
