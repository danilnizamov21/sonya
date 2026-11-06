# sonya/worker/handlers.py


import time

from sonya.core.services.orchestrator import orchestrator_tg
from sonya.core.services.tgstat_service import collect_tgstat


def handle_inspect(task: dict) -> None:
    orchestrator_tg(
        task["status"],
        task["limit"],
        task["batch_size"],
    )


def handle_collect(task: dict) -> None:
    print("принято в обработку")
    collect_tgstat(task["topic"], task["pages"])


def test_handle(task: dict) -> None:
    t_type = task.get("task_type")
    time.sleep(10)
    print(f"ОБРАБОТАНО, {t_type}")


HANDLERS = {"inspect": handle_inspect, "collect": handle_collect, "test": test_handle}


def handle_task(task: dict) -> None:
    task_type = task.get("task_type")

    handler = HANDLERS.get(task_type)

    if handler is None:
        raise ValueError(f"Неизвестный тип задачи: {task_type}")

    handler(task)
