from sonya.services.parsing_service import pars_messages
from sonya.services.telegram_service import inspect_telegram
from sonya.utils.decorators import timer


@timer
def orchestrator_tg(limit: int, batch_size: int):
    inspect_telegram(limit, batch_size)
    pars_messages()
