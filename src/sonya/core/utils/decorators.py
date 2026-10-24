import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        excecution_time = end_time - start_time
        logger.info("Function %s completed in %.2f seconds", func.__name__, excecution_time)
        return result

    return wrapper
