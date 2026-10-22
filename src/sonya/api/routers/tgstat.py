from fastapi import APIRouter, BackgroundTasks

from sonya.api.schemas.tgstat import TopicRequest
from sonya.services.parsing_service import clear_storage
from sonya.services.tgstat_service import collect_tgstat, login_tgstat

router = APIRouter()


@router.post("/collect")
def collect(topic: TopicRequest, background_tasks: BackgroundTasks):
    """Сбор ссылок на тг каналы и сохранение в бд"""
    background_tasks.add_task(
        collect_tgstat,
        topic=topic.topic,
        pages=topic.pages,
    )
    return {"status": "accepted"}


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
