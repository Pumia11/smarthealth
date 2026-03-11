import logging
from typing import Callable, Any
from functools import wraps
import time

from .exceptions import AINetworkError

logger = logging.getLogger(__name__)


def retry_on_network_error(max_retries: int = 2, delay: float = 1.0):
    """网络错误重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except AINetworkError as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Network error on attempt {attempt + 1}/{max_retries + 1}, "
                            f"retrying in {delay}s: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"Max retries exceeded for {func.__name__}")
                        raise
            raise last_exception
        return wrapper
    return decorator
