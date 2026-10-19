from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from sonya.api.schemas.telegram import InspectChannelsRequest, LoginTelegramRequest
from sonya.services.orchestrator import orchestrator_tg
from sonya.services.telegram_service import login_telegram

router = APIRouter()


@router.post("/inspect")
def inspect(payload: InspectChannelsRequest, background_tasks: BackgroundTasks):
    """Сбор HTML с телеграм каналов, парсинг HTML, созранение ссылок в бд"""
    background_tasks.add_task(orchestrator_tg, payload.limit, payload.batch_size)

    return {"Status": "OK"}


@router.post("/login")
def login(payload: LoginTelegramRequest):
    """Создание сессии для Telegram"""
    login_telegram(password=payload.password)
    path_to_image = "src/sonya/session/qr_for_login.png"
    return FileResponse(path_to_image, media_type="image/png")
