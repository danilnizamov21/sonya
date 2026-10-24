from fastapi import APIRouter, BackgroundTasks

from sonya.api.core.job_guard import JobGuard
from sonya.api.schemas.tgstat import TopicRequest
from sonya.core.services.parsing_service import clear_storage
from sonya.core.services.tgstat_service import collect_tgstat, login_tgstat

router = APIRouter()

tgstat_guard = JobGuard("Сбор tg_stat")


@tgstat_guard.releases
def _run_collect_tgstat(topic: str, pages: int) -> None:
    collect_tgstat(topic=topic, pages=pages)


@router.post("/collect")
def collect(topic: TopicRequest, background_tasks: BackgroundTasks):
    """Сбор ссылок на тг каналы и сохранение в бд"""
    tgstat_guard.acquire_or_409()
    background_tasks.add_task(
        _run_collect_tgstat,
        topic=topic.topic,
        pages=topic.pages,
    )
    return {"status": "accepted"}


@router.get("/collect/status")
def collect_status():
    return {"running": tgstat_guard.running}


@router.post("/login")
def login(background_tasks: BackgroundTasks):
    """Создание сессии для TGstat"""
    background_tasks.add_task(login_tgstat)
    return {"status": "accepted"}


@router.delete("/session")
def delete_session():
    clear_storage("src/sonya/collectors/tg_stat/camoufox_profile/")
    if clear_storage is not None:
        return "OK"
    else:
        return "ERROR DELETE STORAGE"
