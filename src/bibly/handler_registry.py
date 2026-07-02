"""Module to manage the registration of handlers for different APIs."""
import logging
from typing import Type, Dict

from bibly.base_handler import SearchHandler

logger = logging.getLogger("bibly")


class HandlerRegistry:
    """
    A registry to manage different search handlers.
    This allows for dynamic loading and management of different search handlers.
    """
    _registry: Dict[str, Type[SearchHandler]] = {}

    @classmethod
    def register_handler(cls, name: str, handler: Type[SearchHandler]):
        cls._registry[name] = handler
    
    @classmethod
    def initialize_handlers(cls, **kwargs) -> Dict[str, SearchHandler]:
        """
        Dynamically initialize all handlers that can be initialized with the given parameters.

        :param kwargs: Parameters to pass to the handlers
        :return: A dictionary of initialized handlers
        """
        initialized_handlers = {}
        for name, handler_class in cls._registry.items():
            if not handler_class.can_initialize(**kwargs):
                missing = [p for p in handler_class.required_params
                           if kwargs.get(p) is None]
                logger.warning(
                    f"{name} not initialized: missing required parameter(s) "
                    f"{missing}"
                )
                continue
            try:
                initialized_handlers[name] = handler_class(**kwargs)
            except Exception as e:
                logger.error(
                    f"{name} failed to initialize: {e}",
                    exc_info=True
                )
        return initialized_handlers

    @classmethod
    def list_handlers(cls) -> list[str]:
        return list(cls._registry.keys())