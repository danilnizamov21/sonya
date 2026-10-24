import threading
from collections.abc import Callable
from functools import wraps

from fastapi import HTTPException


class JobGuard:
    def __init__(self, name: str):
        self.name = name
        self._lock = threading.Lock()

    @property
    def running(self) -> bool:
        return self._lock.locked()

    def acquire_or_409(self) -> None:
        if not self._lock.acquire(blocking=False):
            raise HTTPException(status_code=409, detail="Сбор уже выполняется")

    def releases(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                self._lock.release()

        return wrapper
