"""Module to manage the registration of handlers for different APIs."""
from typing import Type, Dict

from bibly.base_handler import SearchHandler


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
    def get_handler(cls, name: str, **kwargs) -> SearchHandler:
        handler_class = cls._registry.get(name)
        if handler_class and handler_class.can_initialize(**kwargs):
            return handler_class(**kwargs)
        return None
    
    @classmethod
    def initialize_handlers(cls, **kwargs) -> Dict[str, SearchHandler]:
        """
        Dynamically initialize all handlers that can be initialized with the given parameters.

        :param kwargs: Parameters to pass to the handlers
        :return: A dictionary of initialized handlers
        """
        initialized_handlers = {}
        for name, handler_class in cls._registry.items():
            if handler_class.can_initialize(**kwargs):
                initialized_handlers[name] = handler_class(**kwargs)
        return initialized_handlers

    @classmethod
    def list_handlers(cls) -> list[str]:
        return list(cls._registry.keys())