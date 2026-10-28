# sonya/worker/handlers.py


from sonya.core.services.orchestrator import orchestrator_tg
from sonya.core.services.tgstat_service import collect_tgstat


def handle_inspect(task: dict) -> None:
    orchestrator_tg(
        task["status"],
        task["limit"],
        task["batch_size"],
    )


def handle_collect(task: dict) -> None:
    collect_tgstat(task["topic"], task["pages"])


HANDLERS = {
    "inspect": handle_inspect,
    "collect": handle_collect,
}


def handle_task(task: dict) -> None:
    task_type = task.get("task_type")

    handler = HANDLERS.get(task_type)

    if handler is None:
        raise ValueError(f"Неизвестный тип задачи: {task_type}")

    handler(task)
