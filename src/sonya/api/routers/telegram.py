from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from sonya.api.schemas.telegram import InspectChannelsRequest, LoginTelegramRequest
from sonya.core.services.orchestrator import orchestrator_tg
from sonya.core.services.parsing_service import clear_storage
from sonya.core.services.telegram_service import login_telegram

router = APIRouter()
QR_PATH = Path("src/sonya/session/qr_for_login.png")


@router.post("/inspect")
def inspect(payload: InspectChannelsRequest, background_tasks: BackgroundTasks):
    """Сбор HTML с телеграм каналов, парсинг HTML, созранение ссылок в бд"""
    background_tasks.add_task(orchestrator_tg, payload.limit, payload.batch_size)

    return {"Status": "OK"}


@router.post("/login")
def login(payload: LoginTelegramRequest, background_tasks: BackgroundTasks):
    """Создание сессии для Telegram"""
    if QR_PATH.exists():
        QR_PATH.unlink()

    background_tasks.add_task(login_telegram, payload.password)
    return {"status": "starting"}


@router.get("/login/qr")
def get_login_qr():
    if not QR_PATH.is_file():
        raise HTTPException(status_code=409, detail="QR ещё не готов")

    return FileResponse(QR_PATH, media_type="image/png")


@router.delete("/session")
def delete_session():
    clear_storage("src/sonya/collectors/telegram/telegram_profile/")
    if clear_storage is not None:
        return "OK"
    else:
        return "ERROR DELETE STORAGE"
