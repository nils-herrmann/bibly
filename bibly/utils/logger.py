"""Logging decorator for Bibly handlers."""
from typing import Any, Callable, Optional
from functools import wraps
import logging

logger = logging.getLogger("bibly")
logger.setLevel(logging.INFO)
logger.propagate = False

def log_count(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, query: str, *args, **kwargs) -> int:
        try:
            count = func(self, query, *args, **kwargs)
            logger.info(
                f"{self.__class__.__name__} Query: '{query}', Count: {count}"
            )
            return count
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} encountered an error "
                f"with query='{query}': {e}",
                exc_info=True
            )
            raise
    return wrapper


def log_initialization(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        try:
            result = func(self, *args, **kwargs)
            logger.info(f"{self.__class__.__name__} initialized successfully")
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} failed to initialize: {e}",
                exc_info=True
            )
            raise
    return wrapper


def log_search(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, query: str, year_from: Optional[str | int] = None, year_to: Optional[str | int] = None, *args, **kwargs) -> list:
        try:
            result = func(self, query, year_from, year_to, *args, **kwargs)
            logger.info(
                f"{self.__class__.__name__}, "
                f"Query: '{query}', Year From: {year_from}, Year To: {year_to}, "
                f"Results: {len(result)}"
            )
            return result
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} encountered an error "
                f"with query='{query}', year_from={year_from}, year_to={year_to}: {e}",
                exc_info=True
            )
            raise
    return wrapper

def get_logger(name: str = "bibly", log_file: str = "bibly.log", level: int = logging.DEBUG) -> logging.Logger:
    """
    Retrieve and configure a logger.
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (default: logging.DEBUG).
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Avoid adding multiple handlers
        logger.setLevel(level)
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger