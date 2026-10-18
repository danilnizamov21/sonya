from fastapi import APIRouter, BackgroundTasks

from sonya.api.schemas.telegram import InspectChannelsRequest
from sonya.services.telegram_service import inspect_telegram

router = APIRouter()


@router.post("/inspect")
def inspect(payload: InspectChannelsRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(inspect_telegram, payload.limit, payload.batch_size)

    return {"Status": "OK"}
