from fastapi import APIRouter, BackgroundTasks

from sonya.api.schemas.tgstat import TopicRequest
from sonya.services.tgstat_service import collect_tgstat, login_tgstat

router = APIRouter()


@router.post("/collect")
def collect(topic: TopicRequest, background_tasks: BackgroundTasks):
    """Сбор ссылок на тг каналы и сохранение в бд"""
    background_tasks.add_task(collect_tgstat, topic=topic.topic)
    return {"status": "accepted"}


def login(background_tasks: BackgroundTasks):
    """Создание сессии для TGstat"""
    background_tasks.add_task(login_tgstat)
    return {"status": "accepted"}
