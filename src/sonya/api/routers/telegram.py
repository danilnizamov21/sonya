from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from sonya.api.core.job_guard import JobGuard
from sonya.api.core.producer import publish_task
from sonya.api.schemas.telegram import InspectChannelsRequest, LoginTelegramRequest
from sonya.core.services.orchestrator import orchestrator_tg
from sonya.core.services.parsing_service import clear_storage
from sonya.core.services.telegram_service import login_telegram

router = APIRouter()
QR_PATH = Path("src/sonya/session/qr_for_login.png")

inspect_guard = JobGuard("Инспекция каналов")


@inspect_guard.releases
def _run_inspect(status, limit, batch_size):
    orchestrator_tg(status, limit, batch_size)


@router.post("/inspect")
def start_inspect(payload: InspectChannelsRequest):
    publish_task(
        queue_name="sonya.inspect",
        task={
            "task_type": "inspect",
            "limit": payload.limit,
            "batch-size": payload.batch_size,
            "status": payload.status,  # чекаем статутсы которые необходимо, допустиим хотим проверить все доступные каналы - status = accessible и тд.
        },
    )
    return {"task_status": "started"}


@router.get("/inspect/status")
def inspect_status():
    return {"running": inspect_guard.running}


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
