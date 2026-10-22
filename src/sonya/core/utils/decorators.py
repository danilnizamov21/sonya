import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        excecution_time = end_time - start_time
        print(f"Функция {func.__name__}, выполнялась: {excecution_time}")
        return result

    return wrapper
